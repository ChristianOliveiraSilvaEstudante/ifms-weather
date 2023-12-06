
let blockSearch = false

const addInTable = (lat, lon, temperature, feltTemperature, windSpeed, relativeHumidity, seaLevelPressure, uvindex) => {
    const table = document.querySelector('#recent-table')
    table.innerHTML += `
        <tr>
            <td>
                <p>${lat}/${lon}</p>
            </td>
            <td>
                <p>${temperature}</p>
            </td>
            <td>
                <p>${feltTemperature}</p>
            </td>
            <td>
                <p>${windSpeed}</p>
            </td>
            <td>
                <p>${relativeHumidity}</p>
            </td>
            <td>
                <p>${seaLevelPressure}</p>
            </td>
            <td>
                <p>${uvindex}</p>
            </td>
        </tr>
    `
}

const search = async () => {
    if (blockSearch === true) {
        return false
    }

    blockSearch = true

    const lat = document.querySelector('#lat-input').value;
    const lon = document.querySelector('#lon-input').value;

    try {
      const response = await fetch('/weather', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ lat, lon }),
      });
  
      if (response.ok) {
        const data = await response.json();

        addInTable(
            lat,
            lon,
            data.temperature,
            data.felttemperature,
            data.windspeed,
            data.relativehumidity,
            data.sealevelpressure,
            data.uvindex,
        );
      } else {
        console.error('Erro na requisição:', response.status);
      }
    } catch (error) {
      console.error('Erro na execução da requisição:', error);
    } finally {
        blockSearch = false
    }
};

window.onload = () => {
    const button = document.querySelector('#search-button')
    button.onclick = search
}