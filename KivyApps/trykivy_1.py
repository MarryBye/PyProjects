# зовнішній вигляд програми описується в тому (єдиному) екземплярі класу App,
# у якого викликається run().

from kivy.app import App

# Створимо клас-спадкоємець App. У ньому дописуватиметься функціонал програми.


class MyApp(App):
    pass


app = MyApp()
app.run()