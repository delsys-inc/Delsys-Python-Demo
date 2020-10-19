import unittest
from PythonDemo import *

class MyTestCase(unittest.TestCase):
    def test_main(self):
        root = tk.Tk()
        root.geometry('800x750+0+0')
        app = Window(root)
        try:
            app.connect_callback()
            app.scan_callback()

            print("Passed Stage 1")

            app.SensorListbox.select_set(0)
            app.SensorListbox.event_generate("<<ListboxSelect>>")
            listLength = len(app.SensorModeList['values'])
            for i in range(listLength):
                TrigBase.SetSampleMode(0, app.SensorModeList['values'][i])
                actualMode = TrigBase.GetSampleMode()
                self.assertEqual(actualMode[0], app.SensorModeList['values'][i])
            print('Passed Stage 2')

            TrigBase.SetSampleMode(0, app.SensorModeList['values'][0])

            app.init_callback()

            app.start_callback()

            app.stop_callback()

            pass_flag = True
        except:
            pass_flag = False
        self.assertEqual(True, pass_flag)

if __name__ == '__main__':
    unittest.main()
