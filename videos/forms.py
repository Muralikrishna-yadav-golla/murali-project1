from django import forms

class VideoUploadForm(forms.Form):
    video_file = forms.FileField(
        label="Select a Video",
        widget=forms.ClearableFileInput(attrs={'accept': 'video/*', 'class': 'form-control'}),
        required=True
    )
    start_date = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    end_date = forms.DateField(
        label="End Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
