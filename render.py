from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT=Path(__file__).resolve().parent
im=Image.new('RGB',(1024,1024),'#f8f4e8'); d=ImageDraw.Draw(im)
INK='#111111'; RED='#a3121b'; NAVY='#1b3a5c'
def font(n,b=False): return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+('DejaVuSerif-Bold.ttf' if b else 'DejaVuSans.ttf'),n)
def text(s,box,size=18,b=False,color=INK):
 x,y,w,h=box
 for n in range(size,8,-1):
  f=font(n,b); lines=[]
  for p in s.split('\n'):
   line=''
   for word in p.split():
    trial=(line+' '+word).strip()
    if d.textlength(trial,font=f)>w and line: lines.append(line); line=word
    else: line=trial
   lines.append(line)
  step=n+3
  if len(lines)*step<=h: break
 assert len(lines)*step<=h,(s,n)
 for line in lines:
  d.text((x,y),line,font=f,fill=color); y+=step
 return y
def rule(y): d.line((28,y,996,y),fill=INK,width=2)
text('THE WORLD TODAY',(28,15,968,65),61,True)
rule(86)
text('FRIDAY, 20 NOVEMBER 2026',(28,94,470,23),17,True)
text("THE WORLD’S NEWS IN ONE PAGE",(603,94,393,23),16)
rule(124)
text('SHENZHEN SUMMIT',(28,133,968,22),17,True,RED)
text('TRUMP, XI AND PUTIN MEET — AND SIGN A JOINT PEACE PLEDGE',(28,158,968,87),33,True)
text('First-ever three-way meeting in Shenzhen brings a joint declaration committing to peace and stability. Germany’s Chancellor Friedrich Merz warns Europe will accept no new Yalta. An EU–UK summit meets in Brussels the same day.',(28,246,968,67),18)
# Shape-only flag and skyline illustration.
for i in range(3):
 x=28+i*325; y=320; w=318; h=61
 if i==0:
  d.rectangle((x,y,x+w,y+h),fill='white')
  for j in range(13):
   if j%2==0:d.rectangle((x,y+j*h/13,x+w,y+(j+1)*h/13),fill=RED)
  d.rectangle((x,y,x+128,y+33),fill=NAVY)
  for row in range(5):
   for col in range(10): d.ellipse((x+5+col*12,y+3+row*6,x+7+col*12,y+5+row*6),fill='white')
 elif i==1:
  d.rectangle((x,y,x+w,y+h),fill=RED)
  def star(cx,cy,r):
   pts=[(cx+math.cos(-math.pi/2+k*math.pi/5)*(r if k%2==0 else r*.4),cy+math.sin(-math.pi/2+k*math.pi/5)*(r if k%2==0 else r*.4)) for k in range(10)]
   d.polygon(pts,fill='#ffd34a')
  star(x+30,y+27,15)
  for xx,yy in [(54,10),(65,22),(65,37),(54,49)]:star(x+xx,y+yy,5)
 else:
  for j,c in enumerate(['white','#244c99',RED]):d.rectangle((x,y+j*h/3,x+w,y+(j+1)*h/3),fill=c)
for j in range(45):
 x=28+j*22; ht=8+(j*17%25); d.rectangle((x,411-ht,x+17,411),fill=NAVY)
rule(420)
def article(x,y,kicker,headline,body,h=184,w=466):
 text(kicker,(x,y,w,22),16,True,RED)
 end=text(headline,(x,y+24,w,78),23,True)
 text(body,(x,end+5,w,y+h-end-5),17)
article(28,430,'WAR IN UKRAINE','RUSSIA’S BIGGEST BARRAGE HITS KYIV — AND SPILLS INTO POLAND','400+ drones and 110 missiles: 8 killed, about 30 injured. Kyiv bridges and power grid hit. Two Russian missiles land in Poland’s Lublin and Subcarpathian regions; no casualties. Ukraine hits Kerch Bridge and retakes 14 settlements near Kharkiv: Operation Bear Trap, about 200 sq km.',202)
article(530,430,'THE HAGUE','ICJ: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA','The International Court of Justice finds Myanmar committed genocide against the Rohingya in a landmark ruling. The UN chief welcomes the ruling and demands accountability.',202)
rule(641)
article(28,651,'INDIA','CYCLONE AKVAN SLAMS INTO INDIA’S EAST COAST','Landfall near Gopalpur, Odisha, Friday morning. Winds 70–80 km/h, gusting to 90. More than 300,000 evacuated; 423 rescue teams; 69 trains cancelled. No major damage or loss of life reported.',195,w=397)
for r in range(9,33,6): d.arc((445-r,779-r,445+r,779+r),25,310,fill=NAVY,width=3)
article(530,651,'THE GULF','TRUMP PUTS IRAN DECISION OFF TO 2027 AS MISSILES FLY OVER RIYADH','New Iran strikes decision deferred until after 1 January 2027: “I’m not rushing”; “We’ve got time”. US blockade in Strait of Hormuz. Three Houthi missiles intercepted late Friday. A strike damages skyscraper floors in Riyadh’s King Abdullah Financial District; no injuries. Saudi-led forces strike Hodeidah port, Yemen.',195)
d.line((512,430,512,847),fill=NAVY,width=1)
rule(856)
text('ALSO TODAY',(28,864,968,23),17,True,RED)
items=[('COP31 • ANTALYA','Talks run past Friday deadline. Draft drops all fossil-fuel mention; about 200 countries split.'),('ANTHROPIC IPO','Day two: −8.5% to $88.91 after record $81.3bn IPO. Nov. 19 debut: +17% to $97.17.'),('GTA VI RECORD','Rockstar: $3.79bn in first-day sales, an entertainment record after a 13-year wait.'),('FRIDAY MARKETS','Nasdaq −5.28%; S&P 500 −3.70%; Bitcoin $58,939 (−4.79%); WTI $83.62 (+0.49%).')]
for i,(h,b) in enumerate(items):
 x=28+i*245
 text(h,(x,893,232,20),14,True)
 text(b,(x,916,232,72),14)
rule(994)
text('FRIDAY 20 NOVEMBER 2026 • Sources: Reuters, AP, IMD, UN',(28,1000,968,20),13)
(ROOT/'assets').mkdir(exist_ok=True)
im.save(ROOT/'assets/entry.png',optimize=True)
