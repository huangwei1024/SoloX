import json
import os
import traceback
from flask import Blueprint
from flask import render_template
from flask import request
from solox.public.common import Devices,File,Method
from logzero import logger

page = Blueprint("page", __name__)
d = Devices()
m = Method()
f = File()

@page.app_errorhandler(404)
def page_404(e):
    return render_template('404.html', **locals()), 404


@page.app_errorhandler(500)
def page_500(e):
    return render_template('500.html', **locals()), 500


@page.route('/')
def index():
    platform = request.args.get('platform')
    lan = request.args.get('lan')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    return render_template('index.html', **locals())

@page.route('/pk')
def pk():
    lan = request.args.get('lan')
    model = request.args.get('model')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    return render_template('pk.html', **locals())


@page.route('/report')
def report():
    lan = request.args.get('lan')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    report_dir = os.path.join(os.getcwd(), 'report')
    if not os.path.exists(report_dir):
        os.mkdir(report_dir)
    dirs = os.listdir(report_dir)
    dir_list = reversed(sorted(dirs, key=lambda x: os.path.getmtime(os.path.join(report_dir, x))))
    apm_data = []
    for dir in dir_list:
        if dir.split(".")[-1] not in ['log', 'json']:
            try:
                fpath = open(f'{report_dir}/{dir}/result.json')
                json_data = json.loads(fpath.read())
                dict_data = {
                    'scene': dir,
                    'app': json_data['app'],
                    'platform': json_data['platform'],
                    'model': json_data['model'],
                    'devices': json_data['devices'],
                    'ctime': json_data['ctime'],
                }
                fpath.close()
                apm_data.append(dict_data)
            except Exception:
                traceback.print_exc()
                continue
    apm_data_len = len(apm_data)
    return render_template('report.html', **locals())


@page.route('/analysis', methods=['post', 'get'])
def analysis():
    lan = request.args.get('lan')
    scene = request.args.get('scene')
    app = request.args.get('app')
    platform = request.args.get('platform')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    report_dir = os.path.join(os.getcwd(), 'report')
    dirs = os.listdir(report_dir)
    filter_dir = f.filter_secen(scene)
    apm_data = {}
    for dir in dirs:
        if dir == scene:
            try:
                apm_data = f._setAndroidPerfs(scene) if platform == 'Android' else f._setiOSPerfs(scene)
            except ZeroDivisionError:
                pass    
            except Exception:
                traceback.print_exc()
            finally:
                break
    return render_template('analysis.html', **locals())

@page.route('/pk_analysis', methods=['post', 'get'])
def analysis_pk():
    lan = request.args.get('lan')
    scene = request.args.get('scene')
    app = request.args.get('app')
    model = request.args.get('model')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    report_dir = os.path.join(os.getcwd(), 'report')
    dirs = os.listdir(report_dir)
    apm_data = {}
    for dir in dirs:
        if dir == scene:
            try:
                apm_data = f._setpkPerfs(scene)
            except Exception:
                traceback.print_exc()
            finally:
                break
    return render_template('analysis_pk.html', **locals())



@page.route('/compare_analysis', methods=['post', 'get'])
def analysis_compare():
    platform = request.args.get('platform')
    lan = request.args.get('lan')
    scene1 = request.args.get('scene1')
    scene2 = request.args.get('scene2')
    app = request.args.get('app')
    cpuWarning = (0, request.cookies.get('cpuWarning'))[request.cookies.get('cpuWarning') not in [None, 'NaN']]
    memWarning = (0, request.cookies.get('memWarning'))[request.cookies.get('memWarning') not in [None, 'NaN']]
    fpsWarning = (0, request.cookies.get('fpsWarning'))[request.cookies.get('fpsWarning') not in [None, 'NaN']]
    netdataRecvWarning = (0, request.cookies.get('netdataRecvWarning'))[request.cookies.get('netdataRecvWarning') not in [None, 'NaN']]
    netdataSendWarning = (0, request.cookies.get('netdataSendWarning'))[request.cookies.get('netdataSendWarning') not in [None, 'NaN']]
    betteryWarning = (0, request.cookies.get('betteryWarning'))[request.cookies.get('betteryWarning') not in [None, 'NaN']]
    duration = (0, request.cookies.get('duration'))[request.cookies.get('duration') not in [None, 'NaN']]
    solox_host = ('', request.cookies.get('solox_host'))[request.cookies.get('solox_host') not in [None, 'NaN']]
    host_switch = request.cookies.get('host_switch')
    try:
        if platform == 'Android':
            apm_data1 = f._setAndroidPerfs(scene1)
            apm_data2 = f._setAndroidPerfs(scene2)
        elif platform == 'iOS':
            apm_data1 = f._setiOSPerfs(scene1)
            apm_data2 = f._setiOSPerfs(scene2)
    except ZeroDivisionError:
        pass 
    except Exception:
        traceback.print_exc()          
    return render_template('analysis_compare.html', **locals())
