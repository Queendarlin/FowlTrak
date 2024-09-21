document.addEventListener('DOMContentLoaded', function () {
  // Function to fetch data from the API
  async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  }

  // Initialize the Egg Collection Chart
  fetchData('/api/production-data')
    .then((data) => {
      new Chart(
        document.getElementById('eggCollectionChart').getContext('2d'),
        {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: [
              {
                label: 'Egg Collection',
                data: data.data,
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 2,
                tension: 0.1,
              },
            ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  font: {
                    size: 18,
                  },
                },
              },
              x: {
                ticks: {
                  font: {
                    size: 18,
                  },
                },
              },
            },
            plugins: {
              legend: {
                labels: {
                  font: {
                    size: 16,
                  },
                },
              },
              tooltip: {
                bodyFont: {
                  size: 14,
                },
              },
            },
          },
        }
      );
    })
    .catch((error) => console.error('Error fetching production data:', error));

  // Initialize the Symptoms Overview Chart
  fetchData('/api/health-record-data')
    .then((data) => {
      new Chart(document.getElementById('symptomsChart').getContext('2d'), {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: 'Symptoms Overview',
              data: data.data,
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(255, 159, 64, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(54, 162, 235, 0.6)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(54, 162, 235, 1)',
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                font: {
                  size: 18,
                },
              },
            },
            x: {
              ticks: {
                font: {
                  size: 18,
                },
              },
            },
          },
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 18,
                },
              },
            },
            tooltip: {
              bodyFont: {
                size: 18,
              },
            },
          },
        },
      });
    })
    .catch((error) =>
      console.error('Error fetching health record data:', error)
    );

  // Initialize the Flock Distribution Chart
  fetchData('/api/flock-data')
    .then((data) => {
      new Chart(document.getElementById('flockChart').getContext('2d'), {
        type: 'pie',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: 'Flock Distribution',
              data: data.data,
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)',
                'rgba(75, 192, 192, 0.6)',
                'rgba(153, 102, 255, 0.6)',
                'rgba(255, 159, 64, 0.6)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 18,
                },
              },
            },
            tooltip: {
              bodyFont: {
                size: 16,
              },
            },
          },
        },
      });
    })
    .catch((error) => console.error('Error fetching flock data:', error));
});
