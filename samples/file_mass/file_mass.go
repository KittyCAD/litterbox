package main

import (
	"encoding/json"
	"fmt"
	"github.com/kittycad/kittycad.go"
	"os"
	"os/exec"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")

	densitySteelGramsPerCubicMillimeter := 0.00784

	fc, _ := client.File.CreateMass(
		densitySteelGramsPerCubicMillimeter,
		"obj",
		fileBytes,
	)

	fmt.Println("File mass (g): ", fc.Mass)

	json_data, _ := json.Marshal(struct {
		Title string  `json:"title"`
		Mass  float64 `json:"mass"`
	}{
		Title: "output.json",
		Mass:  fc.Mass,
	})

	output_file_path := "./output.json"
	output, _ := os.Create(output_file_path)
	defer output.Close()
	output.Write(json_data)
	if err := output.Sync(); err != nil {
		panic(err)
	}
	exec.Command("cp", "./ORIGINALVOXEL-3.obj", "./output.obj").Output()
}