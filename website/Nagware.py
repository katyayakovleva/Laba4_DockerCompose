from flask import flash


def nagwareInfo():
    flash("Дана версія програми є обмеженою\n  Придбавши повну версію, вам будуть доступні такі можливості:  \n "
          "створювати та видаляти файли, змінювати ім'я файлу, виконувати пошук слів у файлі та поєднувати файли  ",
          category='error')


