from pyjon.reports import ReportFactory

template = 'basic1.xml'
testdata = [range(10)] * 100

if __name__ == '__main__':
    factory = ReportFactory()

    factory.render_template(
            template_file=template,
            title=u'THE TITLE',
            data=testdata,
            dummy='foo'
            )

    factory.render_template(
            template_file=template,
            title=u'THE TITLE 2 :)',
            data=testdata,
            dummy='foo'
            )

    factory.render_document(
            'basic1.pdf')

    factory.cleanup()


