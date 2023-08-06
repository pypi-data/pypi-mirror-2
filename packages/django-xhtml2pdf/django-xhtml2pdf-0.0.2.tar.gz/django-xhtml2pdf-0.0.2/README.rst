Django xhtml2pdf
################


THis project is wrapper code between the django project and the xhtml2pdf
project.

What it does is simply allow people to create xhtml2pdf templates using all the
cool django things like STATIC_URL etc.. (like one would for a webpage
template), and the utils function makes all the images and ressources appear in
the pdf.

Usage
=====

Simply do the following::

    from django_xhtml2pdf.utils import generate_pdf

    def myview(response):
        resp = HttpResponse(content_type='application/pdf')
        result = generate_pdf('my_template.html', file_object=resp)
        return result

