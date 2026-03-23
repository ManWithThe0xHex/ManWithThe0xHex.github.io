---
title: Guía Básica de TCPDUMP
date: 2026-03-23 14:42:12
categories: [Network, security]
tags: [network, security, tcpdump, tcp, sniffing]
image: /assets/Guia-Basica-de-TCPDUMP/tcpdump-structure.png
---

<!--# Guia Básica de TCPDump -->

## Introducción
En el amplio mundo de las redes, la capacidad de analizar y comprender el tráfico de red es fundamental para administradores de sistemas, ingenieros de red y profesionales de seguridad informática. Una herramienta esencial para analisis de redes es `tcpdump`.

**TCPDump** es una herramienta que es usada para analizar los paquetes de datos en una red, nos permite capturar y examinar los paquetes que están siendo transmitidos a través de la red. TCPDump utiliza la biblioteca _libpcap_(escrita en c++) para la captura de paquetes. Esta herramienta es comúnmente preinstalada en muchos sistemas operativos, lo que facilita su acceso y uso en una variedad de entornos de red.


## Fundamentos de TCPDump

### Instalación
```shell
# Ubuntu
sudo apt install tcpdump
# Archlinux
sudo pacman -Syu tcpdump
```

### Mostrar versión
```shell
tcpdump --version
```

### Mostrar Ayuda
```shell
tcpdump --help
man tcpdump
```

## Uso básico

### Respuesta básica tcpdump

![](./assets/Guia-Basica-de-TCPDUMP/tcpdump-structure.png)

### Banderas tcpdump

TCP Flag | tcpdump flag | significado
-|-|-
SYN | S | Paquete SYN - solicita iniciar una connexión
ACK | A | Paquete ACK - Confirma los datos del remitente
FIN| F | Indica la finalización de la conexión
RESET | R | Indica el aborto inmediato de la conexión
PUSH | P | Envia inmediatamente los datos a la aplicacion
URGENT | U | Urgente - Debe ser enviados antes que los datos normales
NONE | . | Usualmente usado como ACK

### Mostramos las interfaces disponibles
Cada interfaz esta asociada a un número
```shell
❯ sudo tcpdump -D

1.enp2s0 [Up, Running, Connected]
2.tun0 [Up, Running, Connected]
3.any (Pseudo-device that captures on all interfaces) [Up, Running]
4.lo [Up, Running, Loopback]
5.bluetooth-monitor (Bluetooth Linux Monitor) [Wireless]
6.nflog (Linux netfilter log (NFLOG) interface) [none]
7.nfqueue (Linux netfilter queue (NFQUEUE) interface) [none]
8.dbus-system (D-Bus system bus) [none]
9.dbus-session (D-Bus session bus) [none]
```


### Captura paquetes en la interfaz por defecto(numero mas bajo en la lista - 1)
Al ejecutar este comando, tcpdump empezará a capturar todos los paquetes que pasen a travez de la interfaz mas baja en la lista de interfaces, en este caso serìa `enp2s0`.
```shell
sudo tcpdump
```

### Captura paquetes en una interfaz especifica
Si queremos capturar paquetes en una interfaz de red diferente, usamos la opción `-i`.
```shell
sudo tcpdump -i tun0
```

### Captura los paquetes en todas las interfaces
Para capturar los paquetes en todas las interfaces usamos la opción `-i` con el valor `any`.
```shell
sudo tcpdump -i any
```

### Capturar paquetes sin resolver direcciones IP y puerto(muestra en numeros)
Si es posible tcpdump nos mostrará el nombre de dominio asociado a la ip y el servicio asociado al puerto; para evitar eso usamos la opción `-n`. Algunas versiones antiguas de tcpdump pueden requerir `-n -n` o `-nn`.
```shell
sudo tcpdump -i enp2s0 -n
```

### Mostrar detalles adicionales con niveles de verbosidad(-v)
```shell
sudo tcpdump -v # Nivel de verbosidad 1
sudo tcpdump -vv # Nivel de verbosidad 2
sudo tcpdump -vvv # Nivel de verbosidad 3
```

### Mostramos direcciones MAC (cabezera de la capa 2)
```shell
sudo tcpdump -e
```

### Mostramos la salida en ASCII - Legible para humanos
```shell
sudo tcpdump -A
```

### Mostramos la salida en hexadecimal
```shell
sudo tcpdump -x
```

### Mostramos la salida en hexadecimal y ascii
```shell
sudo tcpdump -X
```

## Guardar y leer trafico capturado
Si quieres guardar los paquetes capturados en un archivo, usa la opcion `-w` seguido del nombre del archivo a escribir: `-w output.cap`.

```shell
sudo tcpdump -w file
```

Para leer el archivo previamente capturado usamos la opción `-r` seguido del nombre `output.cap`.
```shell
sudo tcpdump -r file
```


## Filtrado de paquetes - Berkeley Packet Filter (BPF)
Una de los aspectos mas poderosos de tcpdump es la capacidad de filtrar paquetes. El lenguaje que usa tcpdump para especificar como filtrar paquetes esta basado en la tecnologia llamada _Berkeley Packet Filter_.

### Calificadores
Los calificadores son modificadores que se utilizan para especificar las condiciones que deben cumplir los paquetes para ser capturados.

Los calificadores basicos se dividen en 3:

#### Tipo:
Con este calificador especificamos el tipo de filtro a aplicar. Existen 4 tipos.
- `host`: Se utiliza para filtrar por una dirección especifica (IPv4 e IPv6)
```shell
sudo tcpdump 'host 192.168.1.33'
```
- `net`: Se utiliza para filtrar por una red en especifico utilizando la notacion CIDR (ejemplo: 192.168.1.0/24)
```shell
sudo tcpdump 'net 192.168.1.0/24'
```
- `port`: Se utiliza para filtrar por un pueto en especifico, puede ser TCP/UPD.
```shell
sudo tcpdump 'port 80'
```
- `portrange`: Se utiliza para filtrar por un rango de puertos en especifico(ejemplo: 67-68. Esto abarca los protocolos TCP/UDP)
```shell
suto tcpdump portrange 136-138
```

##### Direccion

Este calificador se usa para especificar la dirección del flujo de tráfico que deseas filtrar. Existen 4 direcciones.
- `src`: Filtra paquetes con la dirección de origen especificada.
```shell
sudo tcpdump 'src 192.168.1.1'
```
- `dst`: Filtra paquetes con la dirección de destino especificada.
```shell
sudo tcpdump 'dst 192.168.1.1'
```
- `src or dst`: (predeterminado) filtra paquetes con la dirección de origen o destino especificada.
```shell
sudo tcpdump 'src 192.168.1.1 or dst 192.168.1.77'
```

- `src and dst`: Filtra paquetes con ambas direcciones de origen y destino especificadas.
```shell
sudo tcpdump 'src 192.168.1.1 and dst 192.168.1.77'
```

##### Protocolo

Podemos usar este calificador cuando deseamos filtrar el tráfico segun el protocolo:

- Ether, fddi, ip , ip6,  arp, tcp, udp, icmp, icmp6, wlan, etc. Cualquier protocolo soportado por el kernel.

```shell
# filtramos por el protocolo icmp
sudo tcpdump 'icmp'

# filtramos segun los protocolos ip o ipv6
sudo tcpdump 'ip or ipv6'
```

## Combinando multiples expresiones
Multiples expresiones pueden ser combinadas usando las expresiones booleanas
- `and (&&)`
- `or (||)`
- `not, (!)`
- Parentesis para la presedencia. Tambien puede aclarar la intención.

## Ejemplos

### Filtramos paquetes con origen/detino el puerto 53 y protocolo UPD.
```shell
sudo tcpdump 'udp 53'
```

### Filtramos paquetes que tengan como destino el puerto 80
```shell
sudo tcpdump 'dst port 80'
```

### Filtramos paquetes donde la direccion de origen no sea 8.8.8.8

```shell
sudo tcpdump 'not src host 8.8.8.8'
```

### Filtramos paquetes con el protocolo ICMP y direccion de origen 8.8.8.8
```shell
sudo tcpdump 'ICMP and (src host 8.8.8.8)
```

### Filtramos paquetes enviados y recibidos desde/hacia un host/ip
```shell
sudo tcpdump 'host ip'
```

## Recursos
- https://danielmiessler.com/p/tcpdump/
- https://amits-notes.readthedocs.io/en/latest/networking/tcpdump.html
- https://packetlife.net/blog/2011/mar/2/tcp-flags-psh-and-urg/
