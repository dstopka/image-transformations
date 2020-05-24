import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls.Material 2.12
import QtQuick 2.2
import QtQuick.Dialogs 1.3
import QtQuick.Layouts 1.12

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 480
    minimumHeight: 480
    minimumWidth: 800
    title: qsTr("Image transformations")
    Material.theme: Material.Dark

    property int controlsAccent: Material.Purple
    property int controlsBackground: Material.Grey
    property int controlsElevation: 6
    property int paneElevation: 4

    signal outputReady(string s)
    onOutputReady: {
        outputImage.source = s
    }
    signal warning(string message)
    onWarning: {
        warningDialog.text = message
        warningDialog.visible = true
    }
    Component.onCompleted: {
        backend.outputReady.connect(window.outputReady)
        backend.warning.connect(window.warning)
    }

    MessageDialog {
        id: warningDialog
        title: "Warning"
        text: ""
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
        onAccepted: {
        }
    }

    Pane {
        id: mainPanel
        height: parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width < Screen.height * 1.33 ? parent.width : Screen.height * 1.33

        RowLayout {
            id: mainRow
            anchors.fill: parent
            spacing: 15

            Pane {
                id: imagesPane
                Material.elevation: paneElevation
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.minimumHeight: 200
                Layout.minimumWidth: 400

                FileDialog {
                    id: inputFileDialog
                    title: "Please choose a file"
                    folder: shortcuts.pictures
                    onAccepted: {
                        inputImage.source = inputFileDialog.fileUrl
                        backend.load_image(inputFileDialog.fileUrl)
                        outputImage.source = ""
                    }
                    onRejected: {
                    }
                }

                FileDialog {
                    id: outputFileDialog
                    title: "Choose place to save image"
                    folder: shortcuts.pictures
                    selectExisting: false
                    onAccepted: {
                        backend.save_image(outputFileDialog.fileUrl)
                    }
                    onRejected: {
                    }
                }
                Grid {
                    id: imagesColumn
                    rowSpacing: 10
                    columnSpacing: 10
                    anchors.fill: parent
                    columns: 2
                    rows: 3
                    horizontalItemAlignment: Grid.AlignHCenter
                    Button {
                        id: loadButton
                        width: (parent.width - 10) /2
                        Material.foreground: controlsBackground
                        Material.elevation: controlsElevation
                        text: qsTr("LOAD")
                        onClicked: {
                            inputFileDialog.open()
                        }
                    }
                    Button {
                        id: saveButton
                        width: (parent.width - 10) /2
                        Material.foreground: controlsBackground
                        Material.elevation: controlsElevation
                        text: qsTr("SAVE")
                        onClicked: {
                            outputFileDialog.open()
                        }
                    }
                    Label {
                        id: inputLabel
                        text: qsTr("Input Image")
                    }
                    Label {
                        id: outputLabel
                        text: qsTr("Output Image")
                    }
                    Image {
                        id: inputImage
                        Material.elevation: paneElevation
                        width: (parent.width - 10) / 2
                        fillMode: Image.PreserveAspectFit
                        source: ""
                    }
                    Image {
                        id: outputImage
                        Material.elevation: paneElevation
                        width: (parent.width - 10) / 2
                        fillMode: Image.PreserveAspectFit
                        source: ""
                    }
                }
            }
            Pane{
                id: controlsPane
                Material.elevation: paneElevation
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.minimumWidth: 100
                Layout.maximumWidth: 200

                Column{
                    id: controlsColumn
                    anchors.fill: parent
                    spacing: 10

                    ComboBox {
                        id: optionCombo
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        width: parent.width
                        model: ["Histogram", "EntropyFilt", "ImOpen", "Convex"]
                    }

                    Label {
                        id: deviationLabel
                        visible: optionCombo.currentIndex == 0 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        text: qsTr("Deviation")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    TextField {
                        id: deviationInput
                        visible: optionCombo.currentIndex == 0 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        width: parent.width
                        horizontalAlignment: TextInput.AlignHCenter
                        placeholderText: qsTr("Enter number")
                        validator : RegExpValidator { regExp : /[0-9]+\.[0-9]+/ }
                        onTextChanged: {
                            if(text)
                                parameters.deviation = text
                        }
                    }
                    Label {
                        id: maskSizeLabel
                        visible: optionCombo.currentIndex == 1 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        text: qsTr("Mask Size")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    TextField {
                        id: maskSizeInput
                        visible: optionCombo.currentIndex == 1 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        width: parent.width
                        horizontalAlignment: TextInput.AlignHCenter
                        placeholderText: qsTr("Enter number")
                        validator : RegExpValidator { regExp : /[0-9]+\.[0-9]+/ }
                        onTextChanged: {
                            if(text)
                                parameters.mask_size = text
                        }
                    }
                    Label {
                        id: lengthLabel
                        visible: optionCombo.currentIndex == 2 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        text: qsTr("Length")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    TextField {
                        id: lengthInput
                        visible: optionCombo.currentIndex == 2 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        width: parent.width
                        horizontalAlignment: TextInput.AlignHCenter
                        placeholderText: qsTr("Enter number")
                        validator : RegExpValidator { regExp : /[0-9]+\.[0-9]+/ }
                        onTextChanged: {
                            if(text)
                                parameters.length = text
                        }
                    }
                    Label {
                        id: angleLabel
                        visible: optionCombo.currentIndex == 2 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        text: qsTr("Angle")
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    Slider {
                        id: angleSlider
                        visible: optionCombo.currentIndex == 2 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        width: parent.width
                        from: 0
                        value: 0
                        to: 180
                        stepSize: 1
                        onMoved: {
                            parameters.angle = value
                        }
                    }
                    Label {
                        id: angleValueLabel
                        visible: optionCombo.currentIndex == 2 ? true : false
                        Material.foreground: controlsBackground
                        Material.accent: controlsAccent
                        Material.elevation: controlsElevation
                        text: qsTr("Value:") + angleSlider.value
                        anchors.left: parent.left
                    }
                    Button {
                        id: startButton
                        Material.foreground: controlsBackground
                        Material.elevation: controlsElevation
                        width: parent.width
                        text: qsTr("START")
                        onClicked: {backend.transform_image(optionCombo.currentIndex)}
                    }
                    Button {
                        id: histogramButton
                        Material.foreground: controlsBackground
                        Material.elevation: controlsElevation
                        width: parent.width
                        text: qsTr("HISTOGRAMS")
                        onClicked: {backend.show_histograms()}
                    }
                }
            }
        }
    }
}