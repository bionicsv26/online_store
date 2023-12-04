from django.contrib import admin



# @admin.register(Discount)
# class DiscountAdmin(admin.ModelAdmin):
#     list_display = ['name', 'type', 'value']
#     search_fields = 'name', 'type',
#
#
# @admin.register(Seller)
# class SellerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'text_description', 'is_active', 'slug']
#     search_fields = 'name', 'is_active', 'slug',
#     prepopulated_fields = {'slug': ('name',)}
#
#
#     def text_description(self, obj: Seller) -> str:
#         if len(obj.description) < 48:
#             return obj.description
#         return obj.description[:48] + ' ...'
#
#     text_description.short_description = "Краткий текст"
#
#
# @admin.register(SellerProduct)
# class SellerProductAdmin(admin.ModelAdmin):
#     list_display = ['product', 'seller', 'price', 'discount', 'created_at', 'is_active']
#     list_display_links = 'product', 'seller', 'discount',
#     search_fields = 'product', 'seller', 'discount', 'is_active',
