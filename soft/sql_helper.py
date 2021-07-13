from .models import Title, Level, Hashtag

def get_all_titles():
    return Title.objects.all()

def get_all_levels():
    return Level.objects.all()

def get_all_hashtags():
    return Hashtag.objects.all()

def get_all_titles_with_levels(level):
    return Title.objects.raw('SELECT * FROM soft_title WHERE level_id = ' + level)

def get_all_hashtag_with_tiitles(title):
    return Title.objects.raw('SELECT * FROM soft_hashtag WHERE title_id = ' + title)