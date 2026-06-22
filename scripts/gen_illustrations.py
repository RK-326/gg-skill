# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
plt.rcParams['font.family']='DejaVu Sans'
BLUE='#1565c0'; DK='#0b3d6e'; GR='#0b6e4f'; LB='#eef4fb'; GREY='#5b6b7b'
OUT='/tmp/bak_imgs/'

def box(ax,x,y,w,h,text,fc=LB,ec=BLUE,fs=11,tc=DK,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.06",
        fc=fc,ec=ec,lw=1.6))
    ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,color=tc,
        wrap=True,fontweight='bold' if bold else 'normal')
def arrow(ax,x1,y1,x2,y2,color=BLUE):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=16,lw=1.8,color=color))

# 1 TIMELINE
fig,ax=plt.subplots(figsize=(9,2.4)); ax.set_xlim(0,10); ax.set_ylim(0,3); ax.axis('off')
ax.set_title('Дорога к поступлению: месяц за месяцем',fontsize=14,color=DK,fontweight='bold',pad=8)
stages=[("Весна-лето","стажировки,\nолимпиады,\nпрофессора"),
        ("Июль-авг","поиск вузов,\nфинпомощь,\nсписок"),
        ("Авг-сен","Honors,\nCommonApp,\nглавное эссе"),
        ("Сен-окт","Why us,\nпортфолио,\nSAT"),
        ("Ноя-дек","Supplementals,\nдокументы,\nтесты"),
        ("Дек-март","CSS Profile,\nподача\nзаявок")]
ax.plot([0.6,9.4],[1.9,1.9],color=BLUE,lw=2,zorder=1)
for i,(m,t) in enumerate(stages):
    x=0.8+i*1.72
    ax.scatter([x],[1.9],s=240,color=BLUE,zorder=3,edgecolor='white',lw=2)
    ax.text(x,2.55,m,ha='center',va='center',fontsize=10.5,fontweight='bold',color=BLUE)
    ax.text(x,1.0,t,ha='center',va='top',fontsize=8.6,color=GREY)
fig.savefig(OUT+'illus_1.png',dpi=160,bbox_inches='tight'); plt.close(fig)

# 3 GPA scale
fig,ax=plt.subplots(figsize=(8,2.8)); ax.set_xlim(0,10); ax.set_ylim(0,4); ax.axis('off')
ax.set_title('Перевод оценок: 5-балльная → GPA 4.0',fontsize=14,color=DK,fontweight='bold',pad=6)
pairs=[("5.0","4.0"),("4.5","3.6"),("4.0","3.2"),("3.5","2.8"),("3.0","2.4")]
for i,(a,b) in enumerate(pairs):
    x=1.2+i*1.7
    box(ax,x-0.55,2.7,1.1,0.7,a,fc='#eaf1fb',ec=BLUE,fs=13,bold=True)
    box(ax,x-0.55,0.7,1.1,0.7,b,fc='#eaf6ef',ec=GR,fs=13,tc=GR,bold=True)
    arrow(ax,x,2.65,x,1.45,color=GREY)
ax.text(5,3.75,'пятибалльная система',ha='center',fontsize=10,color=BLUE)
ax.text(5,0.35,'американская система (макс. 4.0)',ha='center',fontsize=10,color=GR)
ax.text(5,2.05,'грубый ориентир «для себя»: делим балл на 1.25',ha='center',fontsize=9.5,
        color=GREY,style='italic')
fig.savefig(OUT+'illus_3.png',dpi=160,bbox_inches='tight'); plt.close(fig)

# 6 pyramid reach/target/safe
fig,ax=plt.subplots(figsize=(7.5,4)); ax.set_xlim(0,10); ax.set_ylim(0,6); ax.axis('off')
ax.set_title('Как собрать список вузов (15-25 штук)',fontsize=14,color=DK,fontweight='bold',pad=6)
ax.add_patch(Polygon([[5,5.6],[3.4,3.9],[6.6,3.9]],fc='#c9ddf6',ec=BLUE,lw=1.6))
ax.add_patch(Polygon([[3.4,3.85],[6.6,3.85],[7.4,2.15],[2.6,2.15]],fc='#9bbfe9',ec=BLUE,lw=1.6))
ax.add_patch(Polygon([[2.6,2.1],[7.4,2.1],[8.2,0.4],[1.8,0.4]],fc='#6699d6',ec=BLUE,lw=1.6))
ax.text(5,4.55,'REACH\n3-5 вузов\nIvy / need-blind',ha='center',va='center',fontsize=9.5,color=DK,fontweight='bold')
ax.text(5,3.0,'TARGET\nреально проходите',ha='center',va='center',fontsize=10,color='white',fontweight='bold')
ax.text(5,1.25,'SAFE  ·  3-5 вузов\nвысокий acceptance rate',ha='center',va='center',fontsize=10,color='white',fontweight='bold')
ax.text(8.7,3.0,'всего\n15-25\nвузов',ha='center',va='center',fontsize=10,color=GR,fontweight='bold')
fig.savefig(OUT+'illus_6.png',dpi=160,bbox_inches='tight'); plt.close(fig)

# 8 essay map (tree)
fig,ax=plt.subplots(figsize=(9,3.6)); ax.set_xlim(0,12); ax.set_ylim(0,5); ax.axis('off')
ax.set_title('Карта эссе и лимиты слов',fontsize=14,color=DK,fontweight='bold',pad=6)
box(ax,0.3,2.1,1.9,0.9,'ЭССЕ',fc=BLUE,ec=DK,fs=13,tc='white',bold=True)
nodes=[("Main essay\n600-650 слов",3.9),("Why this university\n200-800 слов",2.7),
       ("Supplementals\n(My world, Readings,\nMy values, Failure…)\n150-500 слов",1.35),
       ("Extracurriculars\n150-500 слов",0.1)]
for t,y in nodes:
    box(ax,4.2,y,4.6,1.0,t,fc=LB,ec=BLUE,fs=9.6)
    arrow(ax,2.2,2.55,4.15,y+0.5,color=GREY)
fig.savefig(OUT+'illus_8.png',dpi=160,bbox_inches='tight'); plt.close(fig)

# 9 SAT structure
fig,ax=plt.subplots(figsize=(9.5,3.2)); ax.set_xlim(0,12); ax.set_ylim(0,4); ax.axis('off')
ax.set_title('Структура цифрового SAT',fontsize=14,color=DK,fontweight='bold',pad=6)
mods=[("Reading &\nWriting · 1","32 мин · 27 вопр."),("Reading &\nWriting · 2","32 мин · 27 вопр."),
      ("Math · 1","35 мин · 22 вопр."),("Math · 2","35 мин · 22 вопр.")]
for i,(a,b) in enumerate(mods):
    x=0.4+i*2.9
    fc='#eaf1fb' if i<2 else '#eaf6ef'; ec=BLUE if i<2 else GR
    box(ax,x,2.0,2.5,1.4,a+"\n\n"+b,fc=fc,ec=ec,fs=10,tc=DK)
    if i<3: arrow(ax,x+2.55,2.7,x+2.85,2.7,color=GREY)
ax.text(6,1.55,'2-й модуль адаптивный: сложность зависит от 1-го',ha='center',fontsize=9.5,color=GREY,style='italic')
ax.text(6,0.8,'800 + 800 = 1600',ha='center',fontsize=14,color=DK,fontweight='bold')
ax.text(6,0.25,'1400 - хорошо    ·    1500+ - отлично',ha='center',fontsize=10,color=GR)
fig.savefig(OUT+'illus_9.png',dpi=160,bbox_inches='tight'); plt.close(fig)

# 12 budget bar
fig,ax=plt.subplots(figsize=(8.5,3.4))
items=['Перелёт + проживание\nдля сдачи SAT','Application fees\n(за все вузы)','Нотариальные\nпереводы','SAT','Duolingo English Test']
lo=[600,300,100,100,59];
ax.barh(items,lo,color=[BLUE,BLUE,BLUE,GR,GR],edgecolor='white')
for i,v in enumerate(lo): ax.text(v+15,i,f'~{v}$',va='center',fontsize=10,color=DK,fontweight='bold')
ax.set_xlim(0,900); ax.set_title('Из чего складывается бюджет (≈ 1500-3000 $ суммарно)',fontsize=13,color=DK,fontweight='bold',pad=8)
ax.tick_params(labelsize=9.5);
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.text(0.99,-0.18,'суммы ориентировочные, проверяйте на официальных сайтах',transform=ax.transAxes,ha='right',fontsize=8.5,color=GREY,style='italic')
fig.savefig(OUT+'illus_12.png',dpi=160,bbox_inches='tight'); plt.close(fig)

print("OK illustrations:", [f for f in ['illus_1','illus_3','illus_6','illus_8','illus_9','illus_12']])
