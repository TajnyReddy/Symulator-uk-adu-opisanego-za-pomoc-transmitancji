Nasz projekt podzieliliśmy na 3 pliki tak, aby był bardziej klarowny i czytelny. 
Pierwszym z nich jest plik gui ,który stworzyliśmy przy pomocy biblioteki PySide6.
Drugi nosi nazwę MplWidget, który tworzy Widget typu Mpl, co pozwala nam na wyświetlenie wykresów w gui.
Ostatnim plikiem jest plik main, w którym oprócz uruchamiania programu umieściliśmy tworzenie wykresów na podstawie danych wprowadzanych w gui. 
Do stworzenia wykresów posłużyliśmy się metodą numerycznych rozwiązań równań stanów, między innymi dlatego, że rozwiązanie z różniczkami nie pozwala  nam na pobudzanie układu sygnałem innym niż harmoniczny.  W naszym rozwiązaniu przypisujemy wartościom macierzy, obliczone wcześniej parametry, ukazane wyżej.
¬Parametry jakie wprowadzamy do programu dotyczące sygnału wejściowego to amplituda oraz ilość przebiegów sygnału. Czas symulacji oraz szybkość próbkowania zostały ustawione na stałe wynoszące kolejno 50 oraz 1000. Nasz program sprawdza różniej stabilność układy, który tworzymy wpisując parametry.  Zaimplementowaliśmy te warunki sprawdzające.
¬¬¬¬Jeżeli nasz układ ich nie spełnia, pojawi się okno proszące o wprowadzenie nowych danych. 
W pola przeznaczone na parametry nie ma możliwości wpisania liter ani znaków niebędących cyframi. Program na podstawie danych wykrywa też stopień mianownika i na jego podstawie sprawdza stabilność całego układu.
