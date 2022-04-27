from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from kivy.uix.screenmanager import Screen, ScreenManager
import json
import requests
from kivymd.uix.list import ThreeLineListItem
import sys
from kivy.properties import StringProperty

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class JanelaGerenciadora(ScreenManager):
    pass

class LastDelivery(Screen):

    def get_post(self,id, pa):
        baseurl = 'https://apiconecttec.ezho.com.br/V3/EcrPaymentReconciliation/LastDelivery?stationId='+id+'&fuelpointNumber='+pa
        response = requests.get(baseurl, headers={'EcrKeyAuthorization': '6746e7f7-435f-4a4e-9e1f-e97b24552576',
                                                  'EcrStationKeyAuthorization': 'c5e68dcb-df52-4d6f-bb91-261c44cdc813'})
        # converter dados
        print(response)
        data = json.dumps(response.json(), indent=4)
        result = json.loads(data)


        for row in result:
            for attribute, value in result.items():

                print(str(value["stationId"]))
                #image = ImageLeftWidget(source=".images/conecttec.png")
                #items = ThreeLineListItem(text= 'StationID: '+str(value['stationId']), secondary_text='Volume: '+ str(value['volume']),
                                   #         tertiary_text= 'Total: '+str(value['total']),)

                self.ids.resposta.text = 'Station: ' + str(value['stationId']) +'\n' + 'ID Abastecimento: ' + \
                                         str(value['deliveryId']) + '\n' + 'Bico: '+ str(value['hoseNumber']) + \
                                         '\n'+ 'Volume: '+ str(value['volume']) + '\n' + 'Total: '+str(value['total']) + '\n' + 'Data e Hora: ' + str(value['dateTime'])
                #self.ids.abastecimento_last.add_widget(items)
    def check_data_login(self):
        username = self.ids.stationID.text
        password = self.ids.PA.text
        print(username)
        print(password)
        LastDelivery.get_post(self,username,password)

class ByFuelPointNumber(Screen):

    scr_mngr = ObjectProperty(None)
    state = StringProperty("stop")


    def get_post(self, id, pa, start, end):
        pass

    def on_save(self, instance, value, date_range):
        filter = ByFuelPointNumber()
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.ids.datetime.text = f'{str(date_range[0])} / {str(date_range[-1])}'
        print(instance, value, date_range)
        id_pos = self.ids.stationID1.text
        position = self.ids.PA1.text
        #filter.get_post(username, password, f'{str(date_range[0])}', f'{str(date_range[-1])}')
        baseurl = 'https://apiconecttec.ezho.com.br/EcrPaymentReconciliation/ByFuelPointNumber?stationId=' + id_pos + '&fuelpointNumber=' + position + '&startDate=' + f'{str(date_range[0])}' + \
                  'T00:00:00' + '&endDate=' + f'{str(date_range[-1])}' + 'T23:59:00'
        response = requests.get(baseurl, headers={'EcrKeyAuthorization': '6746e7f7-435f-4a4e-9e1f-e97b24552576',
                                                  'EcrStationKeyAuthorization': 'c5e68dcb-df52-4d6f-bb91-261c44cdc813'})
        # converter dados
        print(response)
        data = json.dumps(response.json(), indent=4)
        result = json.loads(data)
        print(result)
        i = 0
        try:
            for attribute, value in result.items():
                while i < len(data):

                    print(str(value[i]["stationId"]))

                    print(str(value[i]["dateTime"]))
                    volume = str(value[i]['volume'])
                    datetime = str(value[i]['dateTime'])
                    total = str(value[i]['total'])
                    price = str(value[i]['price'])
                    # image = ImageLeftWidget(source=".images/conecttec.png")
                    items = ThreeLineListItem(text='Data e Hora: ' + datetime , secondary_text='Volume: ' + volume + '  ' + 'Preço: ' + price,
                                              tertiary_text='Total a pagar: ' + total, )
                    print(items)
                    self.ids.abastecimento_last.add_widget(items)
                    i += 1
        except:
            print("fim")


    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    def on_state(self, instance, value):
        {
            "start": self.ids.progress.start,
            "stop": self.ids.progress.stop,
        }.get(value)()


class Conecttec_Sub(MDApp):

    def build(self):
        #return Builder.load_string(KV)
        return Builder.load_file('main.kv')
    def fechar(self):
        self.stop()



    def on_save(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.root.ids.datetime.text = str(date_range)

        print(instance, value, date_range)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def show_date_picker(self):
        sys.setrecursionlimit(5000)
        date_dialog = MDDatePicker(mode="range")
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()



Conecttec_Sub().run()


