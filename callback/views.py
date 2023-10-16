from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, StickerMessage, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent, MemberJoinedEvent, MemberLeftEvent, PostbackEvent
from module import func_callback
import git
import subprocess

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN_LINEBOT)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET_LINEBOT)

@csrf_exempt
def update_server(request):
    if request.method == 'POST':
        repo_path = '/home/zhangmen/zmb_line_bot'
        repo = git.Repo(repo_path)

        try:
            repo.git.pull('origin', 'main')
            # subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'], cwd=repo_path)
            subprocess.check_call(['python', 'manage.py', 'makemigrations'], cwd=repo_path)
            subprocess.check_call(['python', 'manage.py', 'migrate'], cwd=repo_path)
            return JsonResponse({'message': 'Updated PythonAnywhere and migrated sucessfully'}, status=200)
        except git.GitCommandError as e:
            return JsonResponse({'error': 'GitCommandError: {}'.format(e.stderr)}, status=500)
        except subprocess.CalledProcessError:
            return JsonResponse({'error': 'Error executing manage.py commands'}, status=500)
    else:
        return JsonResponse({'error': 'Wrong event type'}, status=400)
    
@csrf_exempt
# Create your views here.
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if '訂位' in mtext:
                        func_callback.Reserver(event)
                    # elif 'happy hour' in mtext.lower() or '快樂時光' in mtext:
                    #     func_callback.HappyHour(event)
                    elif '測試' in mtext:
                        func_callback.reply_message_with_quick_reply(event)
                    elif '酒單' in mtext or '酒款' in mtext: 
                        func_callback.IntrBeerMenuFlex(event)
                    elif '鋁罐' in mtext or '鋁罐介紹' in mtext: 
                        func_callback.IntrCanMenuFlex(event)
                    else: #關鍵字
                        func_callback.Other(event)
                elif isinstance(event.message, StickerMessage):
                    func_callback.SendSticker(event)

            elif isinstance(event, PostbackEvent):
                if len(event.postback.data)>7:
                    func_callback.IntrBeerMenuFlex(event)
                elif event.postback.data[0:4]=="Beer":
                    func_callback.IntrBeerMenuFlex(event)

            elif isinstance(event, FollowEvent):
                #func_callback.WelcomeText(event)
                print('加入好友')

            elif isinstance(event, UnfollowEvent):
                print('取消好友')

            elif isinstance(event, JoinEvent):
                print('進入群組')

            elif isinstance(event, LeaveEvent):
                print('離開群組')

            elif isinstance(event, MemberJoinedEvent):
                print('有人入群')

            elif isinstance(event, MemberLeftEvent):
                print('有人退群')
        
        return HttpResponse()
    else:
        return HttpResponseBadRequest()