from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, StickerMessage, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent, MemberJoinedEvent, MemberLeftEvent, PostbackEvent
from module import func_callback
import git
import subprocess
import requests

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

            # response = requests.post(
            #     'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
            #         username=settings.PYTHONANYWHERE_USER, domain_name=settings.PYTHONANYWHERE_DOMAIN_NAME
            #     ),
            #     headers={'Authorization': 'Token {token}'.format(token=settings.PYTHONANYWHERE_API)}
            # )
            # if response.status_code == 200:
            #     print(f"Reload pythonanywhere web is sucessful. {response.content}")
            # else:
            #     print(f"Reload pythonanywhere web is failed. {response.status_code} : {response.content}")

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
                    elif mtext == '登入':
                        line_login(request)
                    # elif 'happy hour' in mtext.lower() or '快樂時光' in mtext:
                    #     func_callback.HappyHour(event)
                    elif mtext == '酒款介紹':
                        func_callback.reply_message_with_quick_reply(event)
                    elif mtext == '全部': 
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
    
# 開始認證流程
def line_login(request):
    print('開始登入')
    # LINE OAuth URL
    line_oauth_url = "https://access.line.me/oauth2/v2.1/authorize"
    params = {
        "response_type": "code",
        "client_id": settings.LINE_CHANNEL_ID,
        "redirect_uri": settings.LINE_CALLBACK_URL,
        "state": "zhangmen54685508",  # 您應該生成一個隨機狀態並儲存它以驗證回調
        "scope": "profile openid email",
    }
    auth_url = requests.Request('GET', line_oauth_url, params=params).prepare().url
    print('準備轉址')
    print(auth_url)
    return redirect(auth_url)

# 處理回調
def line_callback(request):
    print('轉址成功')
    code = request.GET.get('code')
    state = request.GET.get('state')

    # 驗證狀態
    # ...

    # 使用授權碼獲取訪問令牌
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.LINE_CALLBACK_URL,
        "client_id": settings.LINE_CHANNEL_ID,
        "client_secret": settings.LINE_CHANNEL_SECRET,
    }
    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()

    # 使用訪問令牌獲取用戶資料
    profile_url = "https://api.line.me/v2/profile"
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}"
    }
    profile_response = requests.get(profile_url, headers=headers)
    profile_data = profile_response.json()

    print(profile_data)
    # 在此處處理用戶資料，例如保存到資料庫或登入用戶
    # ...

    return JsonResponse(profile_data)