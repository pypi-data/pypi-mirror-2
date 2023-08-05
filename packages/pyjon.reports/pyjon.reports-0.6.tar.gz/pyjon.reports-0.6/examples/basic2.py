from pyjon.reports import ReportFactory

template = 'basic2.xml'

if __name__ == '__main__':
    factory = ReportFactory()

    factory.render_template(
            template_file=template,
            toto='tata'
            )

    factory.render_document(
            'basic2.pdf')

    factory.cleanup()


