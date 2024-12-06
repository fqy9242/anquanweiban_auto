# coding=gb2312
"""
File : get_all_course.py
Auther : MHY,qht
Created : 2024/12/06 11:20
Last Updated :
Description :
Version :
"""

import requests
import time
import tqdm

# categoryCode_list = [101004007, 101004008, 101004013, 101005001, 101005003, 101007001]
# categoryCode_list = [101001001, 101001002, 101003001, 101003002, 101003003, 101003004,
#                      101003005, 101003006, 101003008, 101003010, 101004001, 101004002,
#                      101004003, 101004004, 101004006, 101004007, 101004008, 101004014,
#                      101005001, 101005002, 101006001, 101007001]

# categoryCode_list = [101003001, 101003002, 101003003, 101003004,
#                      101003005, 101003006, 101003008, 101003010, 101004001, 101004002,
#                      101004003, 101004004, 101004006, 101004007, 101004008, 101004014,
#                      101005001, 101005002, 101006001, 101007001]

userId = '839c3281-de56-48e0-8b4b-6346d11e73b4'
userProjectId = 'bfd661e1-c5dc-44cd-88b6-3bcffa8a2236'
cookie = 'Hm_lvt_05399ccffcee10764eab39735c54698f=1732676463,1732679815,1733403740,1733446109; ' \
         'Hm_lpvt_05399ccffcee10764eab39735c54698f=1733446109; HMACCOUNT=0272137A9475E204; ' \
         'SERVERID=9ee29c682be9356b7648e0eed94165c1|1733446140|1733446108 '
xToken = 'af48e3f5-b08d-4167-bc43-f42233835444'
tenantCode = 53000004
categoryCode_list = []


# 增加重试连接次数
# requests.adapters.DEFAULT_RETRIES = 5


def sleep(seconds):
    for s in tqdm.tqdm(range(seconds)):
        time.sleep(1)


# 获取所有的课程列表
url = 'https://weiban.mycourse.cn/pharos/usercourse/listCategory.do?timestamp=' + str(int(time.time() * 1000) / 1000)
data = {
    "tenantCode": tenantCode,
    "userId": userId,
    "userProjectId": userProjectId,
    "chooseType": 3
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
                  'Safari/537.36 Edg/130.0.0.0',
    'X-Token': xToken
}
res = requests.post(url, headers=header, data=data)
for category in res.json()['data']:
    # 提取 categoryCode 并添加到列表中
    categoryCode_list.append(category['categoryCode'])

for categoryCode in categoryCode_list:
    header = {
        'Cookie': cookie, 'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
            'Safari/537.36 Edg/130.0.0.0', 'X-Token': xToken,
        # 'Connection': 'close'
    }
    data = {
        'tenantCode': tenantCode,  # constant,different for each user
        'userId': userId,  # constant,different for each user
        'userProjectId': userProjectId,  # constant,different for each user
        'chooseType': 3,  # constant,different for each user
        'categoryCode': categoryCode  # different for each category
    }
    time_stamp = str(int(time.time() * 1000) / 1000)
    url = f'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp={time_stamp}'
    # 关闭多余连接
    # s = requests.session()
    # s.keep_alive = False
    rsp1 = requests.post(url, headers=header, data=data)  # 获取课程列表
    course_info_list = rsp1.json()['data']
    print(course_info_list)
    print(f'共有{len(course_info_list)}个课程')
    count = 0
    for course_info in course_info_list:
        count += 1
        print(f'进度: {count}/{len(course_info_list)}')
        # 提取userCourseId和resourceId
        userCourseId = course_info['userCourseId']
        # print(f'userCourseId={userCourseId}')
        resourceId = course_info['resourceId']
        resourceName = course_info['resourceName']
        # print('resourceName:', resourceName)
        # print('userCourseId:', userCourseId, 'resourceId:', resourceId)
        # 发送study请求，获取信息：无
        time_stamp2 = str(int(time.time() * 1000) / 1000)
        url2 = f'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp={time_stamp2}'
        data2 = {
            'tenantCode': tenantCode,
            'userId': userId,
            'courseId': resourceId,
            'userProjectId': userProjectId
        }

        # 关闭多余连接
        # s = requests.session()
        # s.keep_alive = False
        rsp2 = requests.post(url2, headers=header, data=data2)
        # print('study:', rsp2)
        # 发送getCourseUrl请求，获取信息：url4，method_token
        time_stamp3 = str(int(time.time() * 1000) / 1000)
        url3 = f'https://weiban.mycourse.cn/pharos/usercourse/getCourseUrl.do?timestamp={time_stamp3}'
        rsp3 = requests.post(url3, headers=header, data=data2)
        # print(rsp3.json())
        url4 = rsp3.json()['data']

        # 发送请求，获取答题用的相关资源
        data3 = {
            'userProjectId': userProjectId,
            'userId': userId,
            'courseId': resourceId,
            'projectType': 'special',
            'projectId': 'undefined',
            'protocol': 'true',
            'link': 20862,
            'weiban': 'weiban',
            # 'userName': userName
        }

        # 关闭多余连接
        # s = requests.session()
        #
        # s.keep_alive = False

        rsp4 = requests.post(url4, headers=header, data=data3)

        method_token = url4.split('&')[3].split('=')[1]
        # print('method_token:', method_token)
        sleep(20)
        # finnal
        url5 = (f'https://weiban.mycourse.cn/pharos/usercourse/getCaptcha.do?userCourseId={userCourseId}'
                f'&userProjectId={userProjectId}&userId={userId}&tenantCode={tenantCode}')
        data5 = {
        }
        header5 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
                'Safari/537.36 Edg/130.0.0.0'
        }
        # 关闭多余连接
        # s = requests.session()
        # s.keep_alive = False
        rsp5 = requests.post(url5, data=data5, headers=header5)
        # print(f'rsp5={str(rsp5.json())}')
        questionId = rsp5.json()['captcha']["questionId"]

        # time.sleep(10)

        url6 = (f'https://weiban.mycourse.cn/pharos/usercourse/checkCaptcha.do?userCourseId={userCourseId}'
                f'&userProjectId={userProjectId}&userId={userId}&tenantCode={tenantCode}&questionId={questionId}')
        print(url6)
        data6 = {
            # 'coordinateXYs': [{"x": 64, "y": 416}, {"x": 141, "y": 416}, {"x": 218, "y": 410}]
            'coordinateXYs': '[{"x": 64, "y": 416}, {"x": 141, "y": 416}, {"x": 218, "y": 410}]'
        }
        header6 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 '
                'Safari/537.36 Edg/130.0.0.0'
        }
        # 关闭多余连接
        # s = requests.session()
        # s.keep_alive = False
        rsp6 = requests.post(url6, data=data6, headers=header6)
        # print(f'rsp6={rsp6.json()['data']['showText']}')

        method_token = rsp6.json()['data']['methodToken']
        url7 = f'https://weiban.mycourse.cn/pharos/usercourse/v2/{method_token}.do?'
        time_stamp7 = int(time.time())
        data7 = {
            'callback': f'jQuery34107900224573703418_{time_stamp7}',
            'userCourseId': userCourseId,
            'tenantCode': tenantCode,
            '_': f'{time_stamp7}'
        }
        header7 = {
            'Cookie': cookie, 'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 '
                'Safari/537.36 Edg/124.0.0.0'
        }
        # 关闭多余连接
        # s = requests.session()
        # s.keep_alive = False
        rsp7 = requests.post(url7, data=data7, headers=header7)
        print(rsp7.text)
        print(f'{resourceName} 大概率搞定了！')
        if count != len(course_info_list):
            print('下一个')
            sleep(1)
        else:
            print('全部搞定！')
            sleep(3)
