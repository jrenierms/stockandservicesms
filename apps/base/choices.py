from django.utils.translation import gettext_lazy as _


sexual_gender = [
    (1, _('Male')),
    (2, _('Female'))
]


action_type = [
    (1, _('Create')),
    (2, _('List')),
    (3, _('Edit')),
    (4, _('Delete')),
    (5, _('Print')),
    (6, _('Consult'))
]


transaction_type = [
    (1, 'Purchase'),
    (2, 'Sale'),
    (3, 'Sale return'),
    (4, 'Purchase return'),
    (5, 'Positive adjustment'),
    (6, 'Negative adjustment'),
    (7, 'Positive value adjustment'),
    (8, 'Negative value adjustment')
]


colors = [
    ('#fb9902', 'rgba(251,153,2,1)', 'ORANGE'),
    ('#347c98', 'rgba(52,124,152,1)', 'B-G'),
    ('#fc600a', 'rgba(252,96,10,1)', 'R-O'),
    ('#0247fe', 'rgba(2,71,254,1)', 'BLUE'),
    ('#fe2712', 'rgba(254,39,18,1)', 'RED'),
    ('#66b032', 'rgba(102,176,50,1)', 'GREEN'),
    ('#fccc1a', 'rgba(252,204,26,1)', 'Y-O'),
    ('#4424d6', 'rgba(68,36,214,1)', 'B-P'),
    ('#fefe33', 'rgba(254,254,51,1)', 'YELLOW'),
    ('#8601af', 'rgba(134,1,175,1)', 'PURPLE'),
    ('#b2d732', 'rgba(178,215,50,1)', 'Y-G'),
    ('#c21460', 'rgba(194,20,96,1)', 'R-P')
]
