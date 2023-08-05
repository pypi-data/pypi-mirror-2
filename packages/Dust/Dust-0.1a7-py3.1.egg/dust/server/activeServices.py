from dust.util.ymap import YamlMap

activeServices={}

paths=YamlMap('config/activeServices.yaml')
for serviceName in paths.keys():
  moduleName, className=paths[serviceName]
  mod=__import__(moduleName)
  print('dynamic loading module: '+str(dir(mod)))
  cls=mod[className]
  obj=cls()
  activeServices[serviceName]=obj
