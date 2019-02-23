import cx_Freeze

path='./'
cards=[i.strip() for i in open(str(path)+'cards.txt').readlines()]

cx_Freeze.setup(name='BlackJack',
    description='BlackJack Game',
    options={'build_exe':{'packages':['pygame'],
            'include_files':['background.jpg','intro.jpg','cards.txt']}},
             executables=[cx_Freeze.Executable('blackjack11.py')])
