package httpclient

import (
	"errors"
	"log"
	"net/http"
	"os"
	"time"

	"worker-go/internal/models"
)

func SendWeatherData(data models.WeatherPayload) error {
	url := os.Getenv("NEST_API_URL")

	var err error
	var resp *http.Response

	//retry básico
	for i := 1; i <= 3; i++ {
		resp, err = PostJSON(url, data)
		if err == nil && resp.StatusCode < 400 {
			log.Println("Enviado para NestJS com sucesso!")
			return nil
		}

		log.Printf("[Retry %d/3] Erro ao enviar: %v", i, err)
		time.Sleep(2 * time.Second)
	}

	return errors.New("Falha após 3 tentativas")
}
