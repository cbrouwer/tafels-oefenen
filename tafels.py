#!/usr/bin/env python3

import os
import random
import time
import collections
import secrets

oefen_tafels = [9]
aantal_sommen = 20
tijd_tussen_sommen = 3

def current_milli_time():
    return time.time_ns() // 1_000_000

def countdown(t): 
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
      
class tafels():
    totaal_tijd = 0
    sommen_goed = 0
    sommen_fout = 0

    statistieken = {}

    def oefenen(self, aantal_sommen, oefen_tafels):
        os.system('clear')
        self.print_banner(aantal_sommen, oefen_tafels)
        for _ in range(aantal_sommen):
            antwoord = self.som(oefen_tafels)
            if (antwoord):
                self.sommen_goed = self.sommen_goed + 1
            else: 
                self.sommen_fout = self.sommen_fout + 1

            print('Hier komt de volgende som...')
            countdown(tijd_tussen_sommen)
            os.system('clear')

        self.print_statistieken()

    def som(self, oefen_tafels):
        tafel = secrets.choice(oefen_tafels)
        som = random.randint(2, 12)
        start =  current_milli_time()
        antwoord = input('%d x %d = ' % (tafel, som))
        duur = current_milli_time() - start
        self.totaal_tijd = self.totaal_tijd + duur
        antwoord_is_goed = antwoord == str(tafel*som)

        stats = self.statistieken.get(tafel, {'aantal_sommen': 0, 'aantal_goed': 0, 'aantal_fout': 0, 'totaal_tijd': 0})
        stats |= {'aantal_sommen': stats['aantal_sommen']+1, 'totaal_tijd': stats['totaal_tijd'] + duur }
        if (antwoord_is_goed): 
            stats |= {'aantal_goed': stats['aantal_goed'] +1}
            print('Goed! 🤩')
        else:
            stats |= {'aantal_fout': stats['aantal_fout'] +1}
            print('%s is Fout 😓 %d x %d = %s' % (antwoord, tafel, som, str(tafel*som)))
            time.sleep(2) 

        self.statistieken[tafel] = stats
        return antwoord_is_goed

    def print_banner(self, aantal_sommen, oefen_tafels):
        print("****************************************************")
        time.sleep(1) 
        print("Welkom bij Elias Tafel Oefenprogramma!")
        time.sleep(1) 
        print("Vandaag oefenen we %d sommen, van de tafels %s!" % (aantal_sommen, ', '.join(map(str, oefen_tafels))))
        print()
        print("We beginnen over:")
        countdown(6)
        os.system('clear')

    def print_statistieken(self):
        gemiddelde_antwoord_tijd = (self.totaal_tijd / (self.sommen_goed + self.sommen_fout)) / 1000
        print ('Klaar! Je had %d goed en %d fout in gemiddeld %.1f seconden.' % 
            (self.sommen_goed, self.sommen_fout, gemiddelde_antwoord_tijd)
        )
        ordered = collections.OrderedDict(sorted(self.statistieken.items()))
        for tafel, stats in ordered.items():
            print("De tafel van %d:" % tafel)
            if (stats['aantal_sommen'] == stats['aantal_goed']):
                print("\t Je had alles goed!👏", end=' ')
            else:
                print("\t Je had een %d fout (van de %d)." % (stats['aantal_fout'], stats['aantal_sommen']),  end=' ')
            
            gemiddelde_antwoord_tijd = (stats['totaal_tijd'] / stats['aantal_sommen']) / 1000
            if (gemiddelde_antwoord_tijd < 2):
                print("En wow, super snel 🚀🚀 (%.1f s)!!" % gemiddelde_antwoord_tijd)
            elif (gemiddelde_antwoord_tijd < 3):
                print("En lekker snel 🚤 (%.1f s)" % gemiddelde_antwoord_tijd)
            elif (gemiddelde_antwoord_tijd < 4):
                print("En nog net op tijd 🙌 (%.1f s)" % gemiddelde_antwoord_tijd)
            else:
                print("Het moet nog wel een beetje sneller 🐌 (%.1f s)" % gemiddelde_antwoord_tijd)


instance = tafels()
instance.oefenen(aantal_sommen, oefen_tafels)