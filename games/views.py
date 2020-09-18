from django.views.generic import TemplateView

class AnagramGameView(TemplateView):
    template_name = 'games/anagram.html'

class MathGameView(TemplateView):
    template_name = 'games/math.html'