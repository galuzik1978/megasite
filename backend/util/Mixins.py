from django.http import JsonResponse, HttpResponse
from django.template.response import SimpleTemplateResponse
import json
from util import customize


class FormMenuMixin:
    """
    Миксин добавляющий в cintext данные для рендеринга меню пользователя
    """
    header = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Пытаемся прочитать customize из сессии, и если его там нет, подставляем из файла
        context['customize'] = customize
        context['menu'] = (self.request.session.get('menu', context['customize'].desk_config['manager']))
        # Принимаем номер активного пункта меню
        if 'id' in self.request.GET:
            id = int(self.request.GET['id'])
            # Активируем соответствующий пункт меню
            for i, sect in enumerate(context['menu']['sections']):
                if i == id:
                    sect['is_active'] = True
                else:
                    sect['is_active'] = False

        context['header'] = self.header

        if (hasattr(self, 'form_class')):
            context['form_header'] = self.form_class.header
        else:
            context['form_header'] = ""
        # Сохраняем customize в сессию пользователя
        self.request.session['menu'] = context['menu']
        return context


class AjaxableResponseMixin:
    """
    Миксин, добавляющий поддержку Ajax для форм.
    Должен использоваться для object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        # response = super(AjaxableResponseMixin, self).from_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return HttpResponse(form.errors, status=400)

    def form_valid(self, form):
        # response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return SimpleTemplateResponse("ok.html")
        else:
            return SimpleTemplateResponse("ok.html")
