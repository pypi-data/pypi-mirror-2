from django.contrib import admin
from models import Area, Block, PluginType, BlockPath


class AreaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Area, AreaAdmin)


class PluginTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(PluginType, PluginTypeAdmin)


class BlockPathAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlockPath, BlockPathAdmin)


class BlockAdmin(admin.ModelAdmin):
    list_display = ('pk', 'area', 'path', 'position', 'plugin_type')
    list_filter = ('area', )

admin.site.register(Block, BlockAdmin)
