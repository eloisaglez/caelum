<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Grabación en RAM - CanSat</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f9;
        }
        .container {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2980b9;
            margin-top: 30px;
        }
        .highlight {
            background-color: #e8f4fd;
            padding: 15px;
            border-left: 5px solid #3498db;
            margin: 20px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        code {
            background-color: #eee;
            padding: 2px 5px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            color: #c7254e;
        }
        .footer {
            margin-top: 50px;
            font-size: 0.9em;
            color: #7f8c8d;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sistema de Grabación en RAM - CanSat (Versión Optimizada)</h1>
        
        <p>El Arduino Nano 33 BLE utiliza la memoria RAM como una <strong>"Caja Negra"</strong> de seguridad. Esto evita fallos por vibraciones en tarjetas MicroSD y asegura que los datos críticos del vuelo se conserven mientras el dispositivo esté encendido.</p>

        <div class="highlight">
            <strong>Capacidad:</strong> 400 registros (~13 minutos a 1 registro cada 2 segundos).
        </div>

        <h2>Comandos del Monitor Serie (9600 baud)</h2>
        <ul>
            <li><code>PRUEBA</code>: Activa el umbral de <strong>0.5m</strong>. Ideal para laboratorio.</li>
            <li><code>CONCURSO</code>: Activa el umbral de <strong>2.5m</strong>. Para el día del lanzamiento.</li>
            <li><code>GRABAR</code>: Fuerza el inicio de la grabación de forma manual.</li>
            <li><code>BORRAR</code>: Limpia la memoria RAM y resetea la altitud máxima.</li>
            <li><code>CSV</code>: Exporta todos los datos guardados en formato de tabla para Excel.</li>
        </ul>

        <h2>Modos de Operación</h2>
        
        <h3>1. Test de Laboratorio (Manual/Sensible)</h3>
        <p>Diseñado para verificar el funcionamiento de los sensores y la memoria en un entorno controlado:</p>
        <ol>
            <li>Cargar el programa y enviar el comando <code>PRUEBA</code>.</li>
            <li>Levantar el CanSat y bajarlo rápido (mínimo 50 cm).</li>
            <li>El LED empezará a parpadear, indicando que está grabando.</li>
            <li>Enviar <code>CSV</code> para verificar la captura de datos.</li>
        </ol>

        <h3>2. Vuelo Real (Automático)</h3>
        <p>Lógica optimizada para la misión oficial:</p>
        <ol>
            <li>Antes del lanzamiento, enviar el comando <code>CONCURSO</code>.</li>
            <li>El sistema esperará a detectar una caída real (descenso de >2.5m desde el punto más alto).</li>
            <li><strong>IMPORTANTE:</strong> Tras el aterrizaje, <strong>no apagues el CanSat</strong>. Conéctalo al PC y usa el comando <code>CSV</code> antes de desconectar la batería.</li>
        </ol>

        <h2>Formato de Datos Exportados</h2>
        <table>
            <thead>
                <tr>
                    <th>Campo</th>
                    <th>Descripción</th>
                    <th>Unidad</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>ms</strong></td>
                    <td>Tiempo desde el encendido</td>
                    <td>milisegundos</td>
                </tr>
                <tr>
                    <td><strong>temp</strong></td>
                    <td>Temperatura ambiente</td>
                    <td>°C</td>
                </tr>
                <tr>
                    <td><strong>hum</strong></td>
                    <td>Humedad relativa</td>
                    <td>%</td>
                </tr>
                <tr>
                    <td><strong>alt</strong></td>
                    <td>Altitud relativa al suelo</td>
                    <td>metros</td>
                </tr>
                <tr>
                    <td><strong>accX/Y/Z</strong></td>
                    <td>Aceleración en los 3 ejes</td>
                    <td>g</td>
                </tr>
            </tbody>
        </table>

        <h2>Notas Técnicas</h2>
        <ul>
            <li><strong>Volatilidad:</strong> Los datos se pierden si se desconecta la batería antes de hacer el volcado CSV.</li>
            <li><strong>Optimización:</strong> Se utiliza el tipo de dato <code>int16_t</code> para maximizar el espacio disponible en la RAM.</li>
        </ul>

        <div class="footer">
            <strong>Autor:</strong> IES Diego Velázquez<br>
            <strong>Proyecto:</strong> CanSat - Misión 2 (Backup RAM)<br>
            <strong>Fecha:</strong> Febrero 2026
        </div>
    </div>
</body>
</html>
