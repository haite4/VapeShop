from django import forms



PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]




class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int,initial=1)
    update = forms.BooleanField(required=False, 
                                initial=False,
                                widget=forms.HiddenInput)


    def __init__(self, *args, **kwargs):
        show_quantity_field = kwargs.pop('show_quantity_field', True)  
        super().__init__(*args, **kwargs)
        if not show_quantity_field:
            self.fields['quantity'].widget = forms.HiddenInput()  