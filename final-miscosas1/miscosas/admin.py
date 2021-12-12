from django.contrib import admin


from .models import Alimentador, Item, ProfilePhoto, Comentario, Vote

admin.site.register(Alimentador)
admin.site.register(Item)
admin.site.register(ProfilePhoto)
admin.site.register(Comentario )
admin.site.register(Vote)
