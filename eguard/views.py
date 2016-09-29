from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.conf import settings
from eguard.models import Entrance, EntranceAppointment
from mail.sendmail import sendEmail

# Create your views here.

@login_required
def dealAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(EntranceAppointment, id=request.POST['entrance'])
        appointment.has_approved = bool(request.POST.get('check', False))
        appointment.feedback = request.POST['feedback']
        if appointment.has_approved:
            subject = "您的高场核磁中心门禁申请已通过了,等待学校服务器更新！"
            condition="通过"
        else:
            subject = "您的高场核磁中心门禁的申请被拒绝,详细原因请看内容!"
            condition="被拒绝"
        content = """{username}:\n
        \t您的高场核磁中心门禁申请{cond}了.\n
        反馈意见:{feedback}\n
        有什么问题请联系核磁中心管理员mailto:tonyfeng@xmu.edu.cn,电话2186874.
        """.format(username=appointment.user.surname, 
            feedback=appointment.feedback,
            cond=condition
            )

        if sendEmail([appointment.user.email], settings.DEFAULT_FROM_EMAIL, subject, content):
            appointment.feedback += ", 邮件已发送！"
        else:
            appointment.feedback += ", 邮件发送失败！"
 

        appointment.save()

    return redirect( reverse("accounts:profile") )
