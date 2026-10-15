from django.conf import settings
from mybot.models import beer
from linebot import LineBotApi
from linebot.models import (SendMessage, TextSendMessage, StickerSendMessage,
        QuickReply, QuickReplyButton, MessageAction, PostbackAction, TemplateSendMessage,
        CarouselTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
        CarouselColumn,ButtonsTemplate, BubbleContainer, BoxComponent, TextComponent, ImageComponent,
        IconComponent, ButtonComponent, URIAction, FlexSendMessage, SeparatorComponent, 
        RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, CarouselContainer, FillerComponent,
        PostbackAction, TextMessage, PostbackEvent
)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

def CreateRichMenu(event):
    # 藉由 python api 包裝如下
    try:  
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=843),
            selected=False,
            name="Nice richmenu",
            chat_bar_text="Tap here",
            areas=[RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=843),
                action=URIAction(label='Go to line.me', uri='https://line.me'))]
        )
        rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print(rich_menu_id)
        line_bot_api.set_default_rich_menu(rich_menu_id)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

def WelcomeText(event): #歡迎文字
    try:       
        message = [
            TextSendMessage(
                text="歡迎使用掌門訂購機器人!!!"
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

def IntrMenu(event): #功能說明
    try:       
        message = TextSendMessage(    #文字
            text = "需要什麼服務?",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="酒款介紹",
                        data="Beer000")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="訂購",
                        text="/訂購")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="訂單查詢",
                        text="/訂單查詢")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="設備障礙排除",
                        text="/設備障礙排除")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

def IntrBeerMenu(event): #說明酒款
    try:
        beers = beer.objects.all().order_by('id')#讀取資料夾,依照id排序
        beerNum = beers.count()#啤酒數量
        totalPage = int((beerNum)/3)#酒單頁數
        beerlist = []
        beerpage = int(event.postback.data[4:7])#目前頁數

        if beerpage!=totalPage:#酒單產生
            for a in range(3):
                b = beerpage*3+a
                beerlist.append(PostbackTemplateAction(label=str(beers[b].id)+". "+\
                    str(beers[b].cName)+" "+str(beers[b].ABV)+"%",data='Beer'+'%03d'%beerpage+str(beers[b].cName)))
            beerlist.append(PostbackTemplateAction(label="下一頁",data='Beer'+'%03d'%(beerpage+1)))
        else:
             for a in range(beerNum%3):
                b = beerpage*3+a
                beerlist.append(PostbackTemplateAction(label=str(beers[b].id)+". "+\
                    str(beers[b].cName)+" "+str(beers[b].ABV)+"%",data='Beer'+'%03d'%beerpage+str(beers[b].cName)))           

        message = TemplateSendMessage(
            alt_text='掌門酒款介紹',
            template=ButtonsTemplate(
                title='酒款清單',
                text='你要了解哪一款啤酒?',
                actions=beerlist
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

def IntrBeer(event): #說明酒款
    try:
        if event.type=='postback':
            beerName=event.postback.data[7:]  #啤酒名稱
            thebeer = beer.objects.get(cName=beerName)
        if thebeer.Description=='' or thebeer.Description==None:#取代none
            thebeer.Description=' '
        if thebeer.AwardRecord=='' or thebeer.AwardRecord==None:#得獎資訊處理
            AwardRecord=' '
        else:
            AwardRecord="🏆"+thebeer.AwardRecord.replace('\n','\n🏆')

        abv=''
        if int(thebeer.ABV)<10:#酒精強度
            i=0
            while i < (int(thebeer.ABV)/2):
                abv+='🍺'
                i+=1
        else:
            abv='🍺🍺🍺🍺🍺'
        
        ibu=''
        if int(thebeer.IBU)<60:#苦度
            i=0
            while i < (int(thebeer.IBU)/12):
                ibu+='🌿'
                i+=1
        else:
            ibu='🌿🌿🌿🌿🌿'

        bubble = BubbleContainer(
            direction='ltr',
            #hero=ImageComponent(
            #    url='https://images.chinatimes.com/newsphoto/2016-11-01/1024/BD0300_P_04_02.jpg',
            #    size='full',
            #    aspect_ratio='20:13',
            #    aspect_mode='cover',
            #    action=URIAction(uri='https://images.chinatimes.com/newsphoto/2016-11-01/1024/BD0300_P_04_02.jpg', label='label'),
            #),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text=thebeer.cName, weight='bold', size='xl'),
                    TextComponent(text=thebeer.eName, weight='bold', size='xl'),
                    TextComponent(text=thebeer.Style, size='md', margin='sm'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            TextComponent(text='酒精'+str(abv),size='sm',color='#999999',flex=3),
                            TextComponent(text='苦度'+str(ibu),size='sm',color='#999999',flex=3),
                        ]
                    ),
                    SeparatorComponent(color='#0000FF'),
                    TextComponent(text="ABV : "+str(thebeer.ABV)+'%    IBU : '+str(thebeer.IBU)+'    SRM : '+str(thebeer.SRM), size='sm', margin='sm'),
                    TextComponent(text=AwardRecord, weight='bold', color='#666666', size='sm', margin='md', wrap=True),
                    TextComponent(text=thebeer.Feature, color='#666666', size='sm', margin='md', wrap=True),
                    TextComponent(text=thebeer.Description, color='#666666', size='sm', margin='md', wrap=True),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='愛他',uri='tel:0999999999'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='不愛他',uri="http://www.zhangmen.co")
                            )
                        ]
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@血汗釀酒師 2021',
                    color='#888888',size='sm',align='center'),
                ]
            )
        )
        message = FlexSendMessage(alt_text='讓我來介紹『'+thebeer.cName+'』這款啤酒',contents=bubble)

        '''
        beerlist = []
        beerlist.append(CarouselColumn(thumbnail_image_url='https://images.chinatimes.com/newsphoto/2016-11-01/1024/BD0300_P_04_02.jpg',\
            title=thetitle[0:40],text=thedesc[0:60],\
            actions=[PostbackTemplateAction(label='我愛他',data='action=buy&itemid=1'),\
            PostbackTemplateAction(label='我不愛他',data='action=buy&itemid=1'),URITemplateAction(label='我要客訴',\
            uri='http://example.com/1')]))
        message = TemplateSendMessage(
            alt_text=beerName,
            template=CarouselTemplate(
                columns=beerlist
            )
        )
        '''
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

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
            rempage=totalPage%9-1

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
                        contents=[
                            TextComponent(text=str(beers[b].cName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beers[b].eName).replace('None',' ')+' ', weight='bold', size='xl'),
                            TextComponent(text=str(beers[b].Style).replace('None',' ')+' ', size='md', margin='sm'),
                            BoxComponent(
                                layout='baseline',
                                margin='md',
                                contents=[
                                    TextComponent(text='酒精'+str(abv),size='sm',color='#999999',flex=3),
                                    TextComponent(text='苦度'+str(ibu),size='sm',color='#999999',flex=3),
                                ]
                            ),
                            SeparatorComponent(color='#0000FF'),
                            TextComponent(text="ABV : "+str(beers[b].ABV)+'%    IBU : '+str(beers[b].IBU)+'    SRM : '+str(beers[b].SRM), size='sm', margin='sm'),
                            TextComponent(text=AwardRecord, weight='bold', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Malt).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Hop).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Adj).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Feature).replace('None',' ')+' ', color='#666666', size='sm', margin='md', wrap=True),
                            TextComponent(text=str(beers[b].Description).replace('None',' ')+' ', color='#666666', size='sm', margin='sm', wrap=True),
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
                            BoxComponent(
                                layout='horizontal',
                                margin='xxl',
                                contents=[
                                    ButtonComponent(
                                        style='primary',
                                        height='sm',
                                        action=URIAction(label='NTD '+str(beers[b].NT_29L),uri="http://www.zhangmen.co"),
                                    ),
                                    ButtonComponent(
                                        style='secondary',
                                        height='sm',
                                        action=URIAction(label='NTD '+str(beers[b].NT_330ml),uri="http://www.zhangmen.co"),
                                    )
                                ]
                            ),
                            TextComponent(text='Copyright@血汗釀酒師 2021', color='#888888',size='sm',align='center'),
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
                                url='https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip1.jpg',
                                size='full',
                                aspect_ratio='2:3',
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
                            TextComponent(text='Copyright@血汗釀酒師 2021', color='#888888',size='sm',align='center'),
                        ]
                    )
                )
            )
      
        carousel = CarouselContainer(contents=bubbles)
        message = FlexSendMessage(alt_text='客人~酒單來嚕，再請多訂幾桶嘿。',contents=carousel)

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='發生錯誤'))

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
        TextSendMessage(text='發生錯誤'))