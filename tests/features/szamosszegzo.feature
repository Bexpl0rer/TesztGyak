Feature: A beküldött egész számok összegzése

  Scenario: Induláskor az összeg nulla
    Given egy üres számösszegző
    When lekérdezem az összeget
    Then az összeg 0

  Scenario: Pozitív és negatív egész számok összegzése
    Given egy üres számösszegző
    When beküldöm a 8 egész számot
    And beküldöm a -3 egész számot
    And lekérdezem az összeget
    Then az összeg 5

  Scenario: Tört szám elutasítása
    Given egy üres számösszegző
    When beküldöm a 10 egész számot
    And beküldök egy tört számot
    And lekérdezem az összeget
    Then a beküldés 400-as hibakódot ad
    And az összeg 10

  Scenario: Új szám hozzáadása a korábban tárolt számokhoz
    Given a számösszegző már tárol két számot: 7 és 3
    When beküldöm a 4 egész számot
    And lekérdezem az összeget
    Then az összeg 14