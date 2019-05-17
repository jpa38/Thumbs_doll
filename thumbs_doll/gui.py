#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Kivy's module
# import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage

import script
import shutil
import os


# You get RGBA color with link :
# https://www.hexcolortool.com/#4a3097


class ImageDollScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(ImageDollScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.title = 'Thumbs Doll'

        self.size_option()

        # Gestion du chemin d'accès / Access path gui
        self.label_path_url = Label(text='Path or URL', size_hint=(0.3, 1))
        self.input_path_url = TextInput(multiline=True, on_text_validate=self.action_refresh)
        self.raz_input_path_url_button = Button(text='RAZ', size_hint=(0.1, 1), background_color=[255, 0, 0, 1])
        self.raz_input_path_url_button.bind(on_press=self.action_raz_path)

        self.path_url = BoxLayout(orientation='horizontal')
        self.path_url.add_widget(self.label_path_url)
        self.path_url.add_widget(self.input_path_url)
        self.path_url.add_widget(self.raz_input_path_url_button)

        # Gestion du chemin de destination / Objectif's path gui
        self.label_path_destination = Label(text='Destination', size_hint=(0.3, 1))
        self.input_path_destination = TextInput(multiline=False, text=script.get_path_destination())
        self.raz_path_destination_button = Button(text='RAZ', size_hint=(0.1, 1), background_color=[255, 0, 0, 1])
        self.raz_path_destination_button.bind(on_press=self.action_raz_destination)

        self.path_destination = BoxLayout(orientation='horizontal', minimum_height=10)
        self.path_destination.add_widget(self.label_path_destination)
        self.path_destination.add_widget(self.input_path_destination)
        self.path_destination.add_widget(self.raz_path_destination_button)

        # Gestion de la preview / Preview
        self.refresh_button = Button(text='Refresh', size_hint=(1, 1))
        self.refresh_button.bind(on_press=self.action_refresh)

        self.preview = BoxLayout(orientation='horizontal')
        print("image = " + script.get_full_image_name(self.input_path_url.text))
        self.img = Image(source="preview.jpg")
        self.preview.add_widget(self.img)
        self.preview.add_widget(self.refresh_button)
        # self.preview.add_widget(self.refresh_button)

        # Noms / New file name
        self.label_name = Label(text='''New name ? (Empty to keep original's name)''', size_hint=(1.5, 1))
        self.input_name = TextInput(text='', multiline=False)

        self.name = BoxLayout(orientation='horizontal')
        self.name.add_widget(self.label_name)
        self.name.add_widget(self.input_name)

        # Bouton go / GO / RAZ Buttons
        self.remove_button = Button(text='Remove Files', size_hint=(0.2, 1), background_color=[255, 0, 0, 1])
        self.remove_button.bind(on_press=self.action_remove_files)
        self.go_button = Button(text='GO', font_size=32, background_color=[0, 128, 0, 1])
        self.go_button.bind(on_press=self.action_go)

        self.go = BoxLayout(orientation='horizontal')
        self.go.add_widget(self.go_button)
        self.go.add_widget(self.remove_button)

        # Titre Layout principal
        # Add widgets in the principal layout
        self.add_widget(Label(text=self.title, size_hint=(1, 1), font_size=30))
        self.add_widget(self.path_url)
        self.add_widget(self.path_destination)
        self.add_widget(self.preview)
        self.add_widget(self.size_option())
        self.add_widget(self.button_select())

        self.add_widget(self.name)
        self.add_widget(self.go)

    def action_refresh(self, instance):
        """ Action when refresh button is pressed

        Args:
            instance:
        """
        print("Bouton refresh")

        # print(script.is_url(self.input_path_url.text))

        if script.is_url(self.input_path_url.text) == True:
            print("URL Detectée")
            # script.download_image(self.input_path_url.text,
            #                        ".\input\\" + script.get_full_image_name(self.input_path_url.text))
            # works
            script.download_image(self.input_path_url.text,
                                  os.path.join(script.get_path_input(), script.get_full_image_name(self.input_path_url.text)))

            script.download_image(self.input_path_url.text, 'preview.jpg')
            self.image_size = script.get_image_size('preview.jpg')
            self.img.reload()
            print("Action refresh")

        elif script.is_file(self.input_path_url.text) == True:
            print("Path detecté")
            shutil.copyfile(self.input_path_url.text, 'preview.jpg')
            shutil.copyfile(self.input_path_url.text,
                                  os.path.join(script.get_path_input(), script.get_full_image_name(self.input_path_url.text)))
            self.img.reload()

        else:
            print("Input non valid")

    def action_select_all(self, instance):
        """Action when button select ALL is pressed

        Select all the checkboxs

        Args:
            instance:
        """
        print("Bouton select all")
        for checkbox in self.tblo_checkbox:
            checkbox.active = True

    def action_unselect_all(self, instance):
        """Action when button unselect ALL is pressed

        UnSelect all the checkboxs

        Args:
            instance:
        """
        print("Bouton unselect all")
        for checkbox in self.tblo_checkbox:
            checkbox.active = False

    def action_remove_files(self, instance):
        """Action when button Remove is pressed

        Remove all the input/ouput files

        Args:
            instance:
        """
        print("Bouton remove files")
        script.reset_folder(script.get_path_destination())
        script.reset_folder(script.get_path_input())
        script.reset_preview()
        self.img.reload()

    def action_raz_path(self, instance):
        """ Action when button RAZ after path is pressed

        Remove the path

        Args:
            instance:
        """
        print("Bouton raz path")
        self.input_path_url.text = ""

    def action_raz_destination(self, instance):
        """ Action when button RAZ after destination is pressed

        Remove the destination path

        Args:
            instance:
        """
        print("Bouton raz destination")
        self.input_path_destination.text = ""

    def action_go(self, instance):
        """Action when Go's button is pressed

        Args:
            instance:
        """
        print("Bouton go")

        # Ajout des tailles
        lst_a_traiter = []
        # todo empecher cette action si pas de refresh
        if self.check16.active == True and self.image_size >= 16:
            lst_a_traiter.append(16)
        if self.check32.active == True and self.image_size >= 32:
            lst_a_traiter.append(32)
        if self.check64.active == True and self.image_size >= 64:
            lst_a_traiter.append(64)
        if self.check128.active == True and self.image_size >= 128:
            lst_a_traiter.append(128)
        if self.check256.active == True and self.image_size >= 256:
            lst_a_traiter.append(256)
        if self.check512.active == True and self.image_size >= 512:
            lst_a_traiter.append(512)

        if lst_a_traiter == None \
                or self.input_path_url.text == '' \
                or self.input_path_destination.text == '':
            return

        # Determination de la destination
        print(self.input_name.text)
        if self.input_name.text != '':
            # destination_final = os.path.join(self.path_destination, self.input_name)
            final_name = self.input_name.text
        else:
            # destination_final = os.path.join(self.path_destination, script.get_full_image_name(self.input_path_url))

            final_name = script.get_img_name(self.input_path_url.text)

        for px in lst_a_traiter:
            # image_a_traiter = ".\input\\" + script.get_full_image_name(self.input_path_url.text)
            image_a_traiter = os.path.join(script.get_path_input(), script.get_full_image_name(self.input_path_url.text))

            script.resize(image_a_traiter, px, self.input_path_destination.text, final_name)
            # manip(rename + get_url_extension(url), px, url)

    def button_select(self):
        """GUI building for Select / Unselect buttons

        Returns:
            The GUI about the "Select" Button
        """
        self.select_all = Button(text='Select All')
        self.select_all.bind(on_press=self.action_select_all)

        self.deselect_all = Button(text='UnSelect All')
        self.deselect_all.bind(on_press=self.action_unselect_all)

        select = BoxLayout(orientation='horizontal')
        select.add_widget(self.select_all)
        select.add_widget(self.deselect_all)

        return select

    def size_option(self):
        """GUI building for the checkbox

        Returns:
            The GUI about the Checkbox's size
        """
        self.tblo_layout_checkbox = []
        self.tblo_checkbox = []

        # titre- 16px
        # Contruction de la checkbox
        self.check16 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_16 = self.standard_label("16px")
        self.lbl_16.bind(size=self.lbl_16.setter('text_size'))
        # Construction du layout
        self.option16 = BoxLayout(orientation='horizontal')
        self.option16.add_widget(self.check16)
        self.option16.add_widget(self.lbl_16)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option16)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check16)

        # titre- 32px
        # Contruction de la checkbox
        self.check32 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_32 = self.standard_label("32px")
        self.lbl_32.bind(size=self.lbl_32.setter('text_size'))
        # Construction du layout
        self.option32 = BoxLayout(orientation='horizontal')
        self.option32.add_widget(self.check32)
        self.option32.add_widget(self.lbl_32)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option32)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check32)

        # titre- 64px
        # Contruction de la checkbox
        self.check64 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_64 = self.standard_label("64px")
        self.lbl_64.bind(size=self.lbl_64.setter('text_size'))
        # Construction du layout
        self.option64 = BoxLayout(orientation='horizontal')
        self.option64.add_widget(self.check64)
        self.option64.add_widget(self.lbl_64)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option64)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check64)

        # titre- 128px
        # Contruction de la checkbox
        self.check128 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_128 = self.standard_label("128px")
        self.lbl_128.bind(size=self.lbl_128.setter('text_size'))
        # Construction du layout
        self.option128 = BoxLayout(orientation='horizontal')
        self.option128.add_widget(self.check128)
        self.option128.add_widget(self.lbl_128)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option128)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check128)

        # titre- 256px
        # Contruction de la checkbox
        self.check256 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_256 = self.standard_label("256px")
        self.lbl_256.bind(size=self.lbl_256.setter('text_size'))
        # Construction du layout
        self.option256 = BoxLayout(orientation='horizontal')
        self.option256.add_widget(self.check256)
        self.option256.add_widget(self.lbl_256)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option256)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check256)

        # titre- 512px
        # Contruction de la checkbox
        self.check512 = self.standard_checkbox(True)
        # Construction du bouton
        self.lbl_512 = self.standard_label("512px")
        self.lbl_512.bind(size=self.lbl_512.setter('text_size'))
        # Construction du layout
        self.option512 = BoxLayout(orientation='horizontal')
        self.option512.add_widget(self.check512)
        self.option512.add_widget(self.lbl_512)
        # Ajout du layout dans un tableau
        self.tblo_layout_checkbox.append(self.option512)
        # Ajout de la checkbox dans un tableau
        self.tblo_checkbox.append(self.check512)

        # On construit le layout final des checkbox
        options = GridLayout(cols=3)
        for check in self.tblo_layout_checkbox:
            options.add_widget(check)

        return options

    def standard_checkbox(self, active):
        """Specifie the checkbox parameter

        Args:
            active (bool): True to check, False to UnCheck

        Returns:
            The checkbox
        """
        return CheckBox(active=active, size_hint=(1, 1))

    def standard_label(self, name):
        """Specifie the Label parameter

        Args:
            name (str): The text about the checkbox

        Returns:

        """
        return Label(text=name, halign="left", valign="middle", size_hint=(1, 1))


class MyApp(App):
    # The windows's title
    title = 'Thumbs Doll'
    # The windows's icon
    icon = 'img\icon.png'

    def build(self):
        return ImageDollScreen()


if __name__ == '__main__':

    MyApp().run()
