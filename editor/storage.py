from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re

def list_entries():
    """ Returns all the entries inside the storage folder"""

    _,filenames = default_storage.listdir("storage")
    entries = [re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")]
    return sorted(entries)
    
def save_entry(title, content):
    """Saves a entry in the default storage location"""

    filename = f"storage/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    datafile = ContentFile(content)
    default_storage.save(filename, datafile)

def read_entry(title):
    try:
        f = default_storage.open(f"storage/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def delete_entry(title):
    """Delete entries"""
    
    filename = f"storage/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
