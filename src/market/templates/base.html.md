Основные блоки выделенные в базовом (родительском шаблоне)

1) Блок Title

    {% block title %}
    
    {% endblock %}

2) Блок с подключаемыми ссылками и скриптами front-end 

    {% block link_script %}
         {% block additional_link_script %}
         
          {% endblock %}
    {% endblock %}

3) Блок с ярлыками соц сетей и кнопками "Вход", "Профиль", "Главная"

    {% block top_header %}
    
    {% endblock %}

4) Блок с основными элементами header
   1. кнопками "Главная", "Каталог", "Сравнение",
   2. значком-меню "личный кабинет" и корзиной
   3. Меню продуктов
   4. Поисковая строка

    {% block main_header %}
    
    {% endblock %}

5) Блок только с меню продуктами и поисковой строкой

    {% block menu_search_header %}
    
    {% endblock %}

6) Блок для основного контента страницы

    {% block middle %}
    
    {% endblock %}

7) Блок footer с константной информацией и ссылками по рубрикам

    {% block footer %}
    
    {% endblock %}
