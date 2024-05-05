# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template

# from xhtml2pdf import pisa

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import logging
from xhtml2pdf import pisa

logger = logging.getLogger(__name__)

def render_to_pdf(template_src, context_dict={}):
    try:
        template = get_template(template_src)
        html = template.render(context_dict)
        result = BytesIO()
        # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        else:
            logger.error(f"PDF generation error: {pdf.err}")
            return None
    except Exception as e:
        logger.exception("An error occurred while rendering PDF")
        return None
