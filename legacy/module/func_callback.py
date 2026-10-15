from django.conf import settings
from django.db.models import Max
from mybot.models import beer, can
from linebot import LineBotApi
from linebot.models import (SendMessage, TextSendMessage, StickerSendMessage,
        QuickReply, QuickReplyButton, MessageAction, PostbackAction, TemplateSendMessage,
        CarouselTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
        CarouselColumn,ButtonsTemplate, BubbleContainer, BoxComponent, TextComponent, ImageComponent,
        IconComponent, ButtonComponent, URIAction, FlexSendMessage, SeparatorComponent, 
        RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, CarouselContainer, FillerComponent,
        PostbackAction, TextMessage, PostbackEvent, ImagemapArea, ImagemapSendMessage, URIImagemapAction,
        BaseSize
)

import random

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN_LINEBOT)

def WelcomeText(event): #歡迎文字
    try:       
        message = [
            TextSendMessage(
                text=(
                    "感謝您加入『掌門精釀啤酒』好友!(grin)"+
                    "\n"
                    "【掌門精釀】堅持天然\n"+
                    "直接發酵不過濾(beer)\n"+
                    "保留新鮮活酵母(beer)\n"+
                    "不添加非天然香料(beer)\n"+
                    "\n"+
                    "不定期舉辦抽獎活動、\n"+
                    "隨時發送優惠卷等...\n"+
                    "(star)請持續鎖定(star)\n"+
                    "【掌門精釀啤酒 Line@官方】"
                )
            ),
            StickerSendMessage( #圖片
                package_id='11538',
                sticker_id='51626494'
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

def Reserver(event): #訂位圖文
    try:       
        message = [
            TextSendMessage(
                text="您好！\n掌門精釀台灣各分店-電話訂位資訊\nhttps://lihi.cc/Yrg51\n謝謝。"
            ),
            ImagemapSendMessage(
                base_url='https://i.imgur.com/SBBZUFu.png',
                alt_text='電話訂位',
                base_size=BaseSize(height=1024, width=1024),
                actions=[
                    URIImagemapAction(
                        link_uri='https://lihi.cc/Yrg51',
                        area=ImagemapArea(
                            x=0, y=0, width=1024, height=1024
                        )
                    ),
                ],
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def HappyHour(event): #快樂時光
    try:       
        message = [
            TextSendMessage(
                text=
                    "🍻啤酒買二送一🍻\n"+
                    "Beer Buy 2 Get 1 Free\n"+
                    "\n"+
                    "優惠時段✌✌\n"+
                    "\n"+
                    "    〓台北 Taipei〓\n"+
                    "永康店 (捷運 - 東門站)\n"+
                    "週一 至 週五\n"+ 
                    "15:00 - 19:00\n"+
                    "\n"+
                    "    〓台中 Taichung〓\n"+
                    "勤美店 (近 - 廣三SOGO)\n"+
                    "週一 至 週五 \n"+
                    "17:00 - 20:00\n"+
                    "\n"+
                    "文心店 (近 - 文心崇德路口)\n"+
                    "週一 至 週五 \n"+
                    "17:00 - 20:00\n"+
                    "\n"+
                    "        (國定假日除外)"
                ),
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

def Other(event): #一般訊息
    try:
        if len(event.message.text)>1 and beer.objects.filter(cName__icontains=event.message.text).count()>0:#單一酒款
            IntrTheBeer(event)
        elif event.message.text!=',' and len(event.message.text)<6 and beer.objects.filter(Keyword__icontains=event.message.text).count()>0:#關鍵字
            beers = beer.objects.filter(Keyword__icontains=event.message.text)
            KeyWordBeer(event,beers)
        elif ('黑' in event.message.text) and beer.objects.exclude(time='停產').filter(SRM__gt=25).count()>0:#關鍵字
            beers = beer.objects.exclude(time='停產').filter(SRM__gt=25)
            KeyWordBeer(event,beers)
        elif ('不苦' in event.message.text) and beer.objects.exclude(time='停產').filter(IBU__lt=15).count()>0:#關鍵字
            beers = beer.objects.exclude(time='停產').filter(IBU__lt=15)
            KeyWordBeer(event,beers)
        elif ('得獎' in event.message.text) and len(event.message.text)<6:#關鍵字
            beers = beer.objects.exclude(AwardRecord='')
            KeyWordBeer(event,beers)
        elif (event.message.text in ['隨便','青菜',]) and len(event.message.text)<6:#隨機
            beers = beer.objects.filter(cName=get_random())
            KeyWordBeer(event,beers)
        elif (event.message.text in ['台虎','臺虎','台啤','蔡氏','金色三麥','酉鬼','啤酒頭','吉姆老爹']):#黑名單:       
            message = [
                TextSendMessage(text='這裡是『掌門精釀啤酒』，你喝醉了嗎?'),
                StickerSendMessage( #圖片
                package_id='11537',
                sticker_id='52002773'
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        elif ('掌門' in event.message.text):#關鍵字:       
            message = [
                TextSendMessage(text='掌門愛你唷。'),
                StickerSendMessage( #圖片
                package_id='11537',
                sticker_id='52002742'
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        else:       
            message = [
                TextSendMessage(text='感謝您的留言，專員看到後將會回覆您\n謝謝您的耐心等候，並祝您一切順心。'),
            ]
            line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def get_random():
    max_id = beer.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        Beer = beer.objects.filter(pk=pk).first()
        if Beer:
            return Beer

def KeyWordBeer(event,beers): #關鍵字酒單生產
    try:
        bubbles=[]
        for beer in beers:
            if beer.AwardRecord=='' or beer.AwardRecord==None:#得獎資訊處理
                AwardRecord=' '
            else:
                AwardRecord="🏆"+beer.AwardRecord.replace('\n','\n🏆')
            abv=''
            if int(beer.ABV)<10:#酒精強度
                i=0
                while i < (int(beer.ABV)/2):
                    abv+='🍺'
                    i+=1
            else:
                abv='🍺🍺🍺🍺🍺'
            ibu=''
            if int(beer.IBU)<60:#苦度
                i=0
                while i < (int(beer.IBU)/12):
                    ibu+='🌿'
                    i+=1
            else:
                ibu='🌿🌿🌿🌿🌿'
            if len(bubbles)%10==0:
                bubbles=[]
            bubbles.append(#酒單排版
                BubbleContainer(
                    direction='ltr',
                    body=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            TextComponent(text=str(beer.cName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beer.eName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beer.Style).replace('None',' ')+' ', size='md', margin='sm'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text='酒精'+str(abv),size='sm',color='#999999',flex=1),
                                    TextComponent(text='苦度'+str(ibu),size='sm',color='#999999',flex=1),
                                ]
                            ),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text='ABV : '+str(beer.ABV)+'%', size='sm',flex=1),
                                    TextComponent(text='IBU : '+str(beer.IBU), size='sm',flex=1),
                                    TextComponent(text='SRM : '+str(beer.SRM), size='sm',flex=1),
                                ]
                            ),
                            TextComponent(text=AwardRecord, weight='bold', color='#666666', size='md', margin='md', wrap=True),
                            TextComponent(text=str(beer.Feature).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beer.Description).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            BoxComponent(
                                layout='vertical',
                                position='absolute',
                                width='80px',
                                height='30px',
                                background_color='#ff334b',
                                corner_radius='20px',
                                offset_top='15px',
                                offset_end='15px',
                                contents=[
                                    TextComponent(text=str(beer.time).replace('None','停產'),size='md',color='#ffffff',align='center',offset_top='5px'),
                                ]
                            ),    
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(text='Copyright@掌門精釀啤酒 2023', color='#888888',size='sm',align='center'),
                        ]
                    )
                )
            )
            if len(bubbles)%10==0:
                message = FlexSendMessage(alt_text='讓我來跟你說說有什麼啤酒。',contents=CarouselContainer(contents=bubbles))
                line_bot_api.reply_message(event.reply_token,message)
        message = FlexSendMessage(alt_text='讓我來跟你說說有什麼啤酒。',contents=CarouselContainer(contents=bubbles))
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def IntrTheBeer(event): #說明單一酒款
    try:
        thebeer = beer.objects.filter(cName__icontains=event.message.text)#讀取資料

        if thebeer[0].AwardRecord=='' or thebeer[0].AwardRecord==None:#得獎資訊處理
            AwardRecord=' '
        else:
            AwardRecord="🏆"+thebeer[0].AwardRecord.replace('\n','\n🏆')

        abv=''
        if int(thebeer[0].ABV)<10:#酒精強度
            i=0
            while i < (int(thebeer[0].ABV)/2):
                abv+='🍺'
                i+=1
        else:
            abv='🍺🍺🍺🍺🍺'
                
        ibu=''
        if int(thebeer[0].IBU)<60:#苦度
            i=0
            while i < (int(thebeer[0].IBU)/12):
                ibu+='🌿'
                i+=1
        else:
            ibu='🌿🌿🌿🌿🌿'


        bubble=BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    TextComponent(text=str(thebeer[0].cName).replace('None',' ')+' ', weight='bold', size='xl'),
                    TextComponent(text=str(thebeer[0].eName).replace('None',' ')+' ', weight='bold', size='xl'),
                    TextComponent(text=str(thebeer[0].Style).replace('None',' ')+' ', size='md', margin='sm'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            TextComponent(text='酒精'+str(abv),size='sm',color='#999999',flex=1),
                            TextComponent(text='苦度'+str(ibu),size='sm',color='#999999',flex=1),
                        ]
                    ),
                    SeparatorComponent(color='#0000FF'),
                    BoxComponent(
                        layout='baseline',
                        margin='sm',
                        contents=[
                            TextComponent(text='ABV : '+str(thebeer[0].ABV)+'%', size='sm',flex=1),
                            TextComponent(text='IBU : '+str(thebeer[0].IBU), size='sm',flex=1),
                            TextComponent(text='SRM : '+str(thebeer[0].SRM), size='sm',flex=1),
                        ]
                    ),
                    TextComponent(text=AwardRecord, weight='bold', color='#666666', size='md', margin='md', wrap=True),
                    TextComponent(text=str(thebeer[0].Feature).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                    TextComponent(text=str(thebeer[0].Description).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                    BoxComponent(
                        layout='vertical',
                        position='absolute',
                        width='80px',
                        height='30px',
                        background_color='#ff334b',
                        corner_radius='20px',
                        offset_top='15px',
                        offset_end='15px',
                        contents=[
                            TextComponent(text=str(thebeer[0].time).replace('None','停產'),size='md',color='#ffffff',align='center',offset_top='5px'),
                        ]
                    ),    
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@掌門精釀啤酒 2023', color='#888888',size='sm',align='center'),
                ]
            )
        )
     
        message = FlexSendMessage(alt_text='讓我來介紹『'+thebeer[0].cName+'』這款啤酒',contents=bubble)

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def IntrBeerMenuFlex(event): #說明酒款
    try:
        beers = beer.objects.exclude(time='停產').order_by('id','tapNum')#讀取資料夾,依照id排序
        beerNum = beers.count()#啤酒數量
        totalPage = int((beerNum)/9)#酒單頁數
        if event.type=='message':
            beerpage=0
        elif event.type=='postback':
            beerpage = int(event.postback.data[4:7])#目前頁數
        bubbles = []

        if beerpage!=totalPage:
            rempage=9
        else:
            rempage=beerNum%9

        for a in range(rempage):
            b = beerpage*9+a
            if beers[b].AwardRecord=='' or beers[b].AwardRecord==None:#得獎資訊處理
                AwardRecord=' '
            else:
                AwardRecord="🏆"+beers[b].AwardRecord.replace('\n','\n🏆')

            abv=''
            if int(beers[b].ABV)<10:#酒精強度
                i=0
                while i < (int(beers[b].ABV)/2):
                    abv+='🍺'
                    i+=1
            else:
                abv='🍺🍺🍺🍺🍺'
                
            ibu=''
            if int(beers[b].IBU)<60:#苦度
                i=0
                while i < (int(beers[b].IBU)/12):
                    ibu+='🌿'
                    i+=1
            else:
                ibu='🌿🌿🌿🌿🌿'


            bubbles.append(#酒單排版
                BubbleContainer(
                    direction='ltr',
                    body=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            TextComponent(text=str(beers[b].cName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beers[b].eName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beers[b].Style).replace('None',' ')+' ', size='md', margin='sm'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text='酒精'+str(abv),size='sm',color='#999999',flex=1),
                                    TextComponent(text='苦度'+str(ibu),size='sm',color='#999999',flex=1),
                                ]
                            ),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text='ABV : '+str(beers[b].ABV)+'%', size='sm',flex=1),
                                    TextComponent(text='IBU : '+str(beers[b].IBU), size='sm',flex=1),
                                    TextComponent(text='SRM : '+str(beers[b].SRM), size='sm',flex=1),
                                ]
                            ),
                            TextComponent(text=AwardRecord, weight='bold', color='#666666', size='md', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Feature).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Description).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            BoxComponent(
                                layout='vertical',
                                position='absolute',
                                width='80px',
                                height='30px',
                                background_color='#ff334b',
                                corner_radius='20px',
                                offset_top='15px',
                                offset_end='15px',
                                contents=[
                                    TextComponent(text=str(beers[b].time).replace('None','停產'),size='md',color='#ffffff',align='center',offset_top='5px'),
                                ]
                            ),    
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(text='Copyright@掌門精釀啤酒 2023', color='#888888',size='sm',align='center'),
                        ]
                    )
                )
            )

        if beerpage!=totalPage:#下一頁選單
            bubbles.append(
                BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            ImageComponent(
                                url='https://i.imgur.com/9yMH9rm.jpeg',
                                size='full',
                                aspect_ratio='1:1',
                                aspect_mode='cover',
                                gravity='top',
                            ),
                        ],
                    padding_all='0px',
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                            ButtonComponent(style='primary', height='sm',action=PostbackAction(label='下一頁',data='Beer'+'%03d'%(beerpage+1))),
                            TextComponent(text='Copyright@掌門精釀啤酒 2023', color='#888888',size='sm',align='center'),
                        ]
                    )
                )
            )
      
        carousel = CarouselContainer(contents=bubbles)
        message = FlexSendMessage(alt_text='讓我來跟你說說有什麼啤酒。',contents=carousel)

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def IntrCanMenuFlex(event): #說明鋁罐酒款
    try:
        cans = can.objects.exclude(time='停產')#讀取資料夾,依照id排序
        canNum = cans.count()#啤酒數量
        totalPage = int((canNum)/9)#酒單頁數
        if event.type=='message':
            canpage=0
        elif event.type=='postback':
            canpage = int(event.postback.data[4:7])#目前頁數
        bubbles = []

        if canpage!=totalPage:
            rempage=9
        else:
            rempage=canNum%9
        for a in range(rempage):
            b = canpage*9+a

            abv=''
            if int(cans[b].ABV)<10:#酒精強度
                i=0
                while i < (int(cans[b].ABV)/2):
                    abv+='🍺'
                    i+=1
            else:
                abv='🍺🍺🍺🍺🍺'

            bubbles.append(#酒單排版
                BubbleContainer(
                    size='kilo',
                    hero=ImageComponent(
                                url=str(cans[b].image_url),
                                size='full',
                                aspect_ratio='1:1',
                                aspect_mode='cover',
                            ),
                    body=BoxComponent(
                        layout='vertical',
                        spacing='sm',
                        contents=[
                            TextComponent(text=str(cans[b].cName).replace('None',' ')+' ', weight='bold', size='md'),
                            TextComponent(text=str(cans[b].eName).replace('None',' ')+' ', weight='bold', size='sm'),
                            SeparatorComponent(color='#0000FF'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text=str(abv),size='sm',color='#999999',flex=1),
                                    TextComponent(text='酒精濃度 : '+str(cans[b].ABV)+'%',size='xs', margin='md',color='#8c8c8c',flex=0),
                                ]
                            ),
                            TextComponent(text=str(cans[b].Description).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text='NT $'+str(cans[b].NT_330ml).replace('None',' ')+' ',weight='bold', align='end', size='md', margin='md', wrap=True),
                            #ButtonComponent(style='primary', height='sm',action=URIAction(label=str(cans[b].order_text),url=str(cans[b].order_url))),
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                            ButtonComponent(style='primary', height='sm',action=URIAction(label=str(cans[b].order_text),uri=str(cans[b].order_url))),
                        ]
                    )
                )
            )

        if canpage!=totalPage:#下一頁選單
            bubbles.append(
                BubbleContainer(
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            ImageComponent(
                                url='https://i.imgur.com/9yMH9rm.jpeg',
                                size='full',
                                aspect_ratio='1:1',
                                aspect_mode='cover',
                                gravity='top',
                            ),
                        ],
                    padding_all='0px',
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                            ButtonComponent(style='primary', height='sm',action=PostbackAction(label='下一頁',data='Beer'+'%03d'%(canpage+1))),
                            TextComponent(text='Copyright@掌門精釀啤酒 2023', color='#888888',size='sm',align='center'),
                        ]
                    )
                )
            )
      
        carousel = CarouselContainer(contents=bubbles)
        message = FlexSendMessage(alt_text='讓我跟你介紹有哪些鋁罐產品。',contents=carousel)

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))

def SendSticker(event): #回覆表情
    try:       
        message = [
            StickerSendMessage( #圖片
                package_id='11537',
                sticker_id='52002744'
            )
        ]
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='維護中，稍後再試。'))
