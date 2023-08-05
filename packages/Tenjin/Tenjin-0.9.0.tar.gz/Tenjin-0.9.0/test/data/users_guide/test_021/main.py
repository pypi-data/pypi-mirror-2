import tenjin
template = tenjin.Template('views/page.pyhtml')
print(template.script)

### or:
## engine = tenjin.Engine()
## print(engine.get_template('page.pyhtml').script)
