package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/kittycad/kittycad.go"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")
	// LITTERBOX-END-NON-EDITABLE-SECTION

	densitySteelGramsPerCubicMeter := 0.00784

	fc, err := client.File.CreateMass(
		densitySteelGramsPerCubicMeter,
		kittycad.UnitDensityKgm3,
		kittycad.UnitMasG,
		kittycad.FileImportFormatObj,
		fileBytes,
	)

	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(1)
	}

	fmt.Println("File mass (g): ", fc.Mass)

	json_data, _ := json.Marshal(struct {
		Title string  `json:"title"`
		Mass  float64 `json:"mass"`
	}{
		Title: "output.json",
		Mass:  fc.Mass,
	})

	// LITTERBOX-START-NON-EDITABLE-SECTION
	output_file_path := "./output.json"
	output, _ := os.Create(output_file_path)
	defer output.Close()
	output.Write(json_data)
	if err := output.Sync(); err != nil {
		panic(err)
	}

	// Copy the original file to output.obj.
	if err := copyFile("./ORIGINALVOXEL-3.obj", "./output.obj"); err != nil {
		panic(err)
	}

}

func copyFile(src, dst string) error {
	// Open the source file for reading
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	// Create the destination file
	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	// Copy the content from src to dst
	_, err = io.Copy(dstFile, srcFile)
	if err != nil {
		return err
	}

	return nil
}
