package httpclient

import (
	"errors"
	"log"
	"os"

	"your-module/internal/models"
)

func SendWeatherData(data models.WeatherPayload) error {
	url := os.Getenv("NEST_API_URL")

	resp, err := PostJSON(url, data)
	if err != nil {
		return err
	}

	if resp.StatusCode >= 400 {
		log.Println("NestJS retornou erro:", resp.Status)
		return errors.New("erro no NestJS")
	}

	log.Println("Enviado para NestJS com sucesso!")
	return nil
}
