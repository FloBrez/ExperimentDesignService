import streamlit as st
import json
#import plotly.express as px
from datetime import date, datetime
import time
import pandas as pd
import numpy as np
import plotly.express as px
from utils import img_to_bytes

from enum import Enum

class Bundesland(str, Enum):
    BW = 'Baden-Württemberg'
    BY = 'Bayern'
    BE = 'Berlin'
    BB = 'Brandenburg'
    HB = 'Bremen'
    HH = 'Hamburg'
    HE = 'Hessen'
    MV = 'Mecklenburg-Vorpommern'
    NI = 'Niedersachsen'
    NW = 'Nordrhein-Westfalen'
    RP = 'Rheinland-Pfalz'
    SL = 'Saarland'
    SN = 'Sachsen'
    ST = 'Sachsen-Anhalt'
    SH = 'Schleswig-Holstein'
    TH = 'Thüringen'

def get_tax_rate(bundesland: Bundesland) -> float:
    map_bundesland_rates = {
        Bundesland.BW: 0.050,
        Bundesland.BY: 0.035,
        Bundesland.BE: 0.060,
        Bundesland.BB: 0.065,
        Bundesland.HB: 0.050,
        Bundesland.HH: 0.045,
        Bundesland.HE: 0.060,
        Bundesland.MV: 0.060,
        Bundesland.NI: 0.050,
        Bundesland.NW: 0.065,
        Bundesland.RP: 0.050,
        Bundesland.SL: 0.065,
        Bundesland.SN: 0.035,
        Bundesland.ST: 0.050,
        Bundesland.SH: 0.065,
        Bundesland.TH: 0.065
    }
    return map_bundesland_rates.get(bundesland)

st.header('Einfluss von Zinsen auf die Finanzierbarkeit von Immobilien')
st.markdown('_2022-05-27_')

intro = """
Seit Beginn des Jahres sind die Hypothekenzinsen in Deutschland von etwa 1% auf aktuell 2.75% gestiegen. Mit steigenden Zinsen steigt der Schuldendienst, den Immobilienkäufer monatlich aufbringen müssen - sofern denn die Kaufpreise stabil bleiben. Anders gesagt: Mit steigenden Zinsen können sich Immobilienkäufer nur noch einen geringeren Kaufpreis leisten. Im untenstehenden Rechner können Sie eine schnelle Abschätzung machen, wieviel Immobilie Sie sich leisten können - und wie sich dies verändert sollten die Zinsen weiter steigen.

Beachten Sie jedoch, dass steigende Zinsen und ein geringerer maximaler Kaufpreis keineswegs bedeuten müssen, dass Sie sich "weniger Immobilie" leisten können. Es ist nämlich durchaus zu erwarten, dass auch die Preise für Immobilien sinken werden. Was in den letzten Jahre in die andere Richtung lief - sinkende Zinsen führten (neben anderen Faktoren) zu steigenden Preisen - dürfte sich bei steigenden Preisen wieder umkehren. 
"""
st.markdown(intro)


st.subheader('Budgetrechner')
def calc_affordable_principle(zins_bps: int, annuitaet_mtl_eur: float, laufzeit_monate: int) -> float:
    r = zins_bps / 100 / 100 / 12.0
    return round(annuitaet_mtl_eur / (r * (1+r)**laufzeit_monate / ((1+r)**laufzeit_monate-1)), 2)

col1, col2 = st.columns([1, 1])

with col1:
    annuitaet_mtl_eur = st.number_input('Monatliche Rate (in EUR)', min_value=0, value=1000, step=1)
    eigenkapital_eur = st.number_input('Eigenkapital (in EUR)', min_value=0, value=50000, step=1000)
    laufzeit_monate = st.number_input('Laufzeit des Kredits (in Jahren)', min_value=10, max_value=50, value=30) * 12
    
with col2:
    aktueller_zins_bps = st.number_input('Aktueller Zins (in %)', min_value=0.1, max_value=10.0, value=2.75, step=0.05) * 100
    bundesland = Bundesland(st.selectbox('Bundesland', options=[el.value for el in Bundesland]))
    mit_makler = st.selectbox('Makler', options=['Mit Makler', 'Ohne Makler']) == 'Mit Makler'

zins_bps_bereich = range(10, 510, 5)
data = [{
    'Zins_bps': zins_bps,
    'Zins': zins_bps / 100.0, 
    'Max. Kredit': calc_affordable_principle(zins_bps=zins_bps, annuitaet_mtl_eur=float(annuitaet_mtl_eur), laufzeit_monate=laufzeit_monate)
}
for zins_bps in zins_bps_bereich
]
#budget = max_kredit + eigenkapital_eur
t_steuer = get_tax_rate(bundesland)
t_notar = 0.02
t_makler = 0.0357 if mit_makler else 0.00

df = pd.DataFrame(data)\
    .assign(Kredit=lambda x: x['Max. Kredit'].astype(int))\
    .assign(Budget=lambda x: x['Max. Kredit'] + eigenkapital_eur)\
    .assign(Kaufpreis=lambda x: (x.Budget / (1+t_notar+t_steuer+t_makler)).astype(int)) \
    .assign(Grunderwerbsteuer=lambda x: (x.Kaufpreis * t_steuer).astype(int),
    Notarkosten=lambda x: (x.Kaufpreis * t_notar).astype(int),
    Maklerkosten=lambda x: (x.Kaufpreis * t_makler).astype(int)
    )
#st.dataframe(df)


df_res = df.query("Zins == @aktueller_zins_bps / 100").assign(Eigenkapital=eigenkapital_eur)
res = df.query("Zins == @aktueller_zins_bps / 100").to_dict(orient='records')[0]
#st.write(res)

_, m, _ = st.columns(3)
with m:
    st.metric('Maximaler Kaufpreis', value=str(int(res.get('Kaufpreis'))) + ' €')

makler_string = ' Für einen Makler werden weitere 3,57% des Kaufpreises veranschlagt.' if mit_makler else ''

interpretation = """
Bei einem Zins von **{aktueller_zins_bps}%** können Sie sich eine Immobilie bis **maximal {kp}€** leisten. 

Dies errechnet sich wie folgt: Bei einer Annuität in Höhe von {an} € im Monat und einer Laufzeit von {lz} Jahren, können Sie beim aktuellen Zins **maximal Kredit in Höhe von {fk}€** aufnehmen. Zusammen mit Ihrem Eigenkapital in Höhe von {ek}€ haben Sie somit ein maximales Budget in Höhe von {bg}€. Daraus müssen Sie den Kaufpreis der Immobilie selbst bezahlen sowie die Kaufnebenkosten. In {bundesland} wird eine Grunderwerbsteuer von {steuer}% des Kaufpreises erhoben, für Notar und Grundbucheintrag haben wir pauschal 2% angesetzt.{makler_string} Der maximale Kaufpreis ergibt sich aus der Differenz ihres maximalen Budgets abzüglich der Kaufnebenkosten.

|        |Betrag (€)|
|--------|-------:|
|Eigenkapital|{ek}|
|max. Kreditbetrag|+ {fk}|
|Grunderwerbsteuer|- {st}|
|Notar und Grundbucheintrag|- {nt}|
|Makler|- {mk}|
|**Kaufpreis**|= **{kp}**|


""".format(aktueller_zins_bps=round(aktueller_zins_bps / 100, 2), bg=eigenkapital_eur + res.get('Kredit'),
bundesland=bundesland.value, steuer=round(t_steuer * 100, 2), makler_string = makler_string,
ek=int(eigenkapital_eur), fk=res.get('Kredit'), kp=int(res.get('Kaufpreis')),
mk=res.get('Maklerkosten'), st=res.get('Grunderwerbsteuer'), nt=res.get('Notarkosten'),
an=annuitaet_mtl_eur, lz=int(laufzeit_monate / 12)
)



st.markdown(interpretation)


##################################
# st.metric('Max. Kaufpreis (vor Kaufnebenkosten):', value=200000)
zins_up = aktueller_zins_bps + 100
zins_dn = aktueller_zins_bps - 100

res_up = df.query("Zins == @zins_up / 100").to_dict(orient='records')[0]
res_dn = df.query("Zins == @zins_dn / 100").to_dict(orient='records')[0]

#st.write(res_up)
#st.write(res_dn)

sensibilitaet = """

Ein **Zinsanstieg um einen Prozentpunkt auf {zu}%** reduziert den maximalen Kaufpreis um {zu_d}€ auf {zu_kp}€ ({zu_dl}%). Sollten Hypothekenzinsen jedoch wieder **um einen Prozentpunkt auf {zd}% fallen**, erhöhte sich der maximale Kaufpreis um {zd_d}€ auf {zd_kp}€ ({zd_dl}%).
""".format(zu=zins_up/100, zu_kp=res_up.get('Kaufpreis'), zu_d=res.get('Kaufpreis')-res_up.get('Kaufpreis'), zu_dl=-round((res.get('Kaufpreis')-res_up.get('Kaufpreis'))/res.get('Kaufpreis')*100, 2),
zd=zins_dn/100, zd_kp=res_dn.get('Kaufpreis'), zd_d=res_dn.get('Kaufpreis')-res.get('Kaufpreis'), zd_dl=-round((res.get('Kaufpreis')-res_dn.get('Kaufpreis'))/res.get('Kaufpreis')*100, 2)
)

st.markdown(sensibilitaet)

l, m, r = st.columns(3)
with l:
    st.metric('Maximaler Kaufpreis bei Zinsrückgang um 1%-Punkt', value=str(int(res_dn.get('Kaufpreis'))) + ' €', delta=str(-round((res.get('Kaufpreis')-res_dn.get('Kaufpreis'))/res.get('Kaufpreis')*100, 2)) + '%' )
with m:
    st.metric('Maximaler Kaufpreis', value=str(int(res.get('Kaufpreis'))) + ' €')

with r:
    st.metric('Maximaler Kaufpreis bei Zinsanstieg', value=str(int(res_up.get('Kaufpreis'))) + ' €', delta=str(-round((res.get('Kaufpreis')-res_up.get('Kaufpreis'))/res.get('Kaufpreis')*100, 2)) + '%')

st.markdown('In nachfolgender Graphik sehen Sie den maximalen Kaufpreis für Zinsen von 0% bis 5%:')

fig = px.line(
        df, 
        x='Zins',
        y='Kaufpreis',
        labels={
            'Kaufpreis': 'max. Kaufpreis',
            'Zins': 'Zins (in %)'
        },
    )
fig.update_layout(yaxis={"dtick":50000,"range":[0,df.Budget.max()*1.1]}, 
                            xaxis={"dtick":0.5})
fig.update_layout(yaxis_ticksuffix = '€', yaxis_tickformat = ',.')

fig.add_vline(x=aktueller_zins_bps/100.0, line_width=1, line_dash="dash")
fig.add_annotation(x=aktueller_zins_bps/100, y=0,
            text="Aktueller Sollzins",
            showarrow=False,
            xanchor='left',
            xshift=10,
            yshift=10)


st.plotly_chart(fig, use_container_width=True)

#st.write('{:11.d}'.format(eigenkapital_eur))


