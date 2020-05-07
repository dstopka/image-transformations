import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.3

//---------MAIN WINDOW---------------

Window {
    id: window
    visible: true
    width: 640
    height: 620
    color: "#333333"
    minimumHeight: 620
    minimumWidth: 640
    title: qsTr("image transformations")

    Image {
        id: image_output
        width: parent.width * 0.4
        height: parent.width * 0.4
        anchors.right: parent.right
        anchors.rightMargin: parent.width * 0.05
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.1
        fillMode: Image.PreserveAspectFit
        source: "qrc:/qtquickplugin/images/template_image.png"
    }

    Image {
        id: image_input
        width: parent.width * 0.4
        height: parent.width * 0.4
        anchors.left: parent.left
        anchors.leftMargin: parent.width * 0.05
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.1
        fillMode: Image.PreserveAspectFit
        source: "qrc:/qtquickplugin/images/template_image.png"
    }

    Label {
        id: label_input
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.05
        anchors.left: parent.left
        anchors.leftMargin: parent.width * 0.25 - this.width/2
        text: qsTr("Input Image")
    }

    Label {
        id: label_output
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.05
        anchors.right: parent.right
        anchors.rightMargin: parent.width * 0.25 - this.width/2
        text: qsTr("Output Image")
    }

    Button {
        id: button_load
        width: parent.width * 0.4
        anchors.left: parent.left
        anchors.leftMargin: parent.width * 0.05
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.125 + parent.width * 0.4
        text: qsTr("Load Image")
    }

    Button {
        id: button_save
        width: parent.width * 0.4
        anchors.right: parent.right
        anchors.rightMargin: parent.width * 0.05
        anchors.top: parent.top
        anchors.topMargin: parent.height * 0.125 + parent.width * 0.4
        text: qsTr("Save Image")
    }

    Rectangle {
        id: rectangle_lower_section
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        width: parent.width
        height: parent.height - (parent.width * 0.4 + parent.height * 0.22)





    Rectangle {
        id: rectangle_buttons
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        width: parent.width * 0.25
        height: parent.height
        color: "#424242"

        Button {
            id: button
            x: 15
            y: 13
            text: qsTr("Histogram")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: button1
            x: 15
            y: 59
            text: qsTr("Entropy")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: button2
            x: 15
            y: 107
            text: qsTr("ImOpen")
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Button {
            id: button3
            x: 15
            y: 155
            text: qsTr("Convex")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }


        Rectangle {
            id: rectangle_settings
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            width: parent.width * 0.75
            height: parent.height
            color: "#424242"
    }

        Rectangle {
            id: buttons_settings_border
            anchors.left: rectangle_buttons.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: -1
            width: 2
            height: parent.height - 1
            color: "#353535"
        }
    }

    Rectangle {
        id: image_section_border
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.top: rectangle_lower_section.top
        anchors.topMargin: -1
        width: parent.width
        height: 2
        color: "#000000"
    }


}
