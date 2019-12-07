from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.garden.graph import Graph, MeshLinePlot
from random import gauss
import math

Builder.load_string("""
#:import MeshLinePlot kivy.garden.graph.MeshLinePlot
<MainScreen>:
    Label:
    BoxLayout:
        orientation:'vertical'
        Label:
            text: 'AWGN Channel Analysis' 
            font_size:'30dp'
        Label:
            text: 'Group 5 Division-A  Batch-A1,\\n Mobile Communication Lab,\\n ECED, SVNIT, Surat'
            font_size:'20dp'  
        Label: 
        BoxLayout:
            orientation : 'horizontal'
            Button:
                text: 'Enter'
                font_size:'30dp'
                on_press: root.manager.current = 'Second'
            Button:
                text: 'Exit'
                font_size:'30dp'
                on_press: app.stop()       

<SecondScreen>:
    ti:t
    BoxLayout:
        orientation:'vertical'
        Label:  
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: 'Random Number'
                font_size:'20dp'
                on_press: t.text=''
            TextInput:
                id:t
                multiline:False             
        BoxLayout:
            orientation : 'horizontal'
            Button:
                text: 'Calculate'
                font_size:'20dp'
                on_press:root.awgn_noise()   
            Button:
                text: 'SNR\\nVs\\nBER graph'
                font_size:'20dp'
                on_press:root.manager.current='AWGN'   
            Button:
                text: 'Back'
                font_size:'20dp'
                on_press: root.manager.current = 'Main'
            Button:
                text: 'Exit'
                font_size:'20dp'
                on_press: app.stop()
        Label:

<AWGN>:
    graph_test : graph_test
    Graph:
        id: graph_test
        #plot: MeshLinePlot
        xlabel:'SNR'
        ylabel:'BER'
        x_ticks_minor:1
        x_tics_major:1
        y_ticks_major:0.1
        y_grid_label:True
        x_grid_label:True
        padding:5
        x_grid:True
        y_grid:True
        xmin:1
        xmax:15
        ymin:-2
        ymax:0
        pos: 0, root.height / 6
        size: root.width * 9.5 / 10 , root.height * 18 / 24 

<AWGNScreen>:
    BoxLayout:
        orientation:'vertical' 
        BoxLayout:
            orientation:'horizontal'
            Button:
                text:'Refresh'
                font_size:'30dp'
                on_press:root.update_graph()  
                size: root.width/2, 100
                size_hint: None, None                
            Button:
                text:'Back'
                font_size:'30dp'
                on_press:root.manager.current='Second'  
                size: root.width/2, 100
                size_hint: None,None
""")


class MainScreen(Screen):
    pass


class SecondScreen(Screen):
    ti = ObjectProperty()
    t = StringProperty('')
    data = []

    def awgn_noise(self):
        self.t = self.ti.text
        temp = self.t
        random_number = int(temp)
        bit_stream = [0 if (i % random_number == 0) else 1 for i in range(0, 50)]
        x = 15
        snr_value = [i for i in range(1, x + 1)]
        noise = [gauss(0.0, 1.0) for i in range(len(bit_stream))]
        ber_value = [0.0 for i in range(0, len(snr_value))]
        for i in range(0, len(snr_value)):
            recovered = [bit_stream[u] + noise[u] * (x - i) / x for u in range(0, len(bit_stream))]
            recovered = [0 if (recovered[j] < 0.5) else 1 for j in range(0, len(bit_stream))]
            recovered = [abs(recovered[j] - bit_stream[j]) for j in range(0, len(bit_stream))]
            ber_value[i] = sum(recovered) / len(bit_stream)+1e-2
        print(ber_value)
        ber_value = [math.log10(ber_value[j]) for j in range(0, len(snr_value))]
        self.data.clear()
        self.data.append(snr_value)
        self.data.append(ber_value)
        return


class AWGN(Widget):
    graph_test = ObjectProperty()

    def update_graph(self):
        SS = SecondScreen()
        x = SS.data[0]
        y = SS.data[1]
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x[i], y[i]) for i in range(len(x))]
        self.graph_test.add_plot(plot)


class AWGNScreen(Screen):
    awgn = AWGN()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.awgn)

    def update_graph(self):
        self.awgn.update_graph()


sm = ScreenManager()
sm.add_widget(MainScreen(name='Main'))
sm.add_widget(SecondScreen(name='Second'))
sm.add_widget(AWGNScreen(name='AWGN'))


class AWGNApplication(App):
    def build(self):
        return sm


if __name__ == '__main__':
    AWGNApplication().run()
