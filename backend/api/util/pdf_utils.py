import string
import subprocess
from pathlib import Path
import tempfile
import shutil
import os
import glob
import secrets
from django.conf import settings
import PyPDF2
#from ..models import ContractText

def to_png(filename):
    file_base = filename.replace(".pdf", "")
    for f in glob.glob("%s*preview*" % (file_base)):
        os.remove(f)

    cmd = ["pdftoppm", "-f",  "1", "-l", "3", "-png", "-r", "96",
           filename, "%s-preview" % (file_base)]

    subprocess.Popen(cmd).wait()

def blur_png(filename):
    file_base = filename.replace(".pdf", "")
    for png in glob.glob("%s*preview-*.png" % (file_base)):
        cmd = ["convert", "-region", "816x1056+413x0", "-blur", "0x8",
               png, png.replace(".png", "-blurred.png")]
        subprocess.Popen(cmd).wait()

def to_pdf(filename):
    preview = filename.replace('.pdf', '')
    cmd = ["convert", "%s*preview-*-blurred.png" % (preview), "-quality", "100", "%s-preview.pdf" % (preview)]

    subprocess.Popen(cmd).wait()
    for f in glob.glob("%s-preview-*.png" % (preview)):
        os.remove(f)

    return "%s-preview.pdf" % (preview)


def word_to_pdf(filename):
    import sys
    loffdir = '/opt/libreoffice5.0/program'
    sys.path[0:0] = [ loffdir ]
    os.environ['URE_BOOTSTRAP'] = 'vnd.sun.star.pathname:{0}/fundamentalrc'.format(loffdir)
    #import uno

    outfile = filename.replace(".doc", ".pdf")
    cmd = ["unoconv", "--output=%s" % (outfile), filename]
    print(" ".join(cmd))
    subprocess.Popen(cmd).wait()
    return outfile

def clean_text(text):
    s = list(filter(lambda x: x != '', text.split(' ')))
    return ' '.join(s).replace('\n', ' ')


def extract_text(filename):
    pdf_file = open(filename,'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    text = ''
    for index in range(number_of_pages):
        page = read_pdf.getPage(index)
        page_content = clean_text(page.extractText())
        text += ' ' + page_content
    return text


BASE = Path(__file__).parent


def generate_contract_subdirectory(length = 4):
    alphabet = string.ascii_letters #+ string.digits
    subdir = ''
    while True:
        subdir= ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in subdir)
                and any(c.isupper() for c in subdir)):
                #and sum(c.isdigit() for c in password) >= 1):
            break
    return subdir


def process(filename):
    path = Path(filename)
    base = str(path.parent)
    name = "%s.pdf" % (secrets.token_urlsafe(32))

    with tempfile.TemporaryDirectory() as temp_dir:
        #move to the new temporary directory
        temp_file = os.path.join(temp_dir, name)
        shutil.move(filename, temp_file)
        os.chdir(temp_dir)
        print("...generating preview...")
        to_png(name)
        blur_png()
        blurred_pdf = to_pdf(name)
        print("...extracting text...")
        text = extract_text(name, 1001)
        ct = ContractText(contract_text = text)
        ct.save()
        # move the preview and renamed PDF to the contract directory
        final_dir = os.path.join(settings.CONTRACT_DIR,
                                 generate_contract_subdirectory())
        try:
            os.makedirs(final_dir)
        except Exception as e:
            pass

        #switch to upload to S3 once AWS is setup
        final_pdf_file = os.path.join(final_dir, name)
        shutil.move(temp_file, final_pdf_file)

        preview_name = "%s-preview.pdf" % (secrets.token_urlsafe(32))

        final_preview_file = os.path.join(final_dir, preview_name)
        shutil.move(blurred_pdf, final_preview_file)

        os.chdir(BASE)

        return {
            'pdf': final_pdf_file,
            'preview': final_preview_file,
            'contract_text': ct
        }
