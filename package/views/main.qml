import QtQuick 2.9
import QtQuick.Window 2.2
import QtQuick.Controls 2.3

//---------MAIN WINDOW---------------

Window {
    id: window
    visible: true
    width: 640
    height: 480
    color: "#202020"
    minimumHeight: 480
    minimumWidth: 640
    title: qsTr("image transformations")

    Rectangle {
        id:rectangle_content
        height: parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.height * 1.33
        color: "#333333"

        Rectangle {
            id: rectangle_top_section
            width: parent.width
            height: Math.max(parent.height * 0.7, parent.height - 200)
            anchors.left: parent.left
            anchors.top: parent.top
            color: "transparent"

            Image {
                id: image_output
                width: parent.height * 0.7
                height: parent.height * 0.7
                anchors.right: parent.right
                anchors.rightMargin: parent.width * 0.05
                anchors.top: parent.top
                anchors.topMargin: parent.height * 0.1
                fillMode: Image.PreserveAspectFit
                source: "qrc:/qtquickplugin/images/template_image.png"
            }

            Image {
                id: image_input
                width: parent.height * 0.7
                height: parent.height * 0.7
                anchors.left: parent.left
                anchors.leftMargin: parent.width * 0.05
                anchors.top: parent.top
                anchors.topMargin: parent.height * 0.1
                fillMode: Image.PreserveAspectFit
                source: "qrc:/qtquickplugin/images/template_image.png"
            }

            Label {
                id: label_input
                color: "#ffffff"
                anchors.bottom: image_input.top
                anchors.bottomMargin: 5
                anchors.left: parent.left
                anchors.leftMargin: parent.height * 0.4 - this.width/2
                text: qsTr("Input Image")
            }

            Label {
                id: label_output
                color: "#ffffff"
                anchors.bottom: image_output.top
                anchors.bottomMargin: 5
                anchors.right: parent.right
                anchors.rightMargin: parent.height * 0.4 - this.width/2
                text: qsTr("Output Image")
            }

            Rectangle {
                id: button_load
                width: parent.height * 0.7
                height: 35
                anchors.left: parent.left
                anchors.leftMargin: parent.width * 0.05
                anchors.bottom: parent.bottom
                anchors.bottomMargin: parent.height * 0.05
                color: "#5b5b5b"
                border.color: "#353535"
                radius: 4
                Text {
                    id: text_button_load
                    text: qsTr("Load Image")
                    anchors.centerIn: parent
                    font.pixelSize: 9
                    color: '#ffffff'
                }
                MouseArea {
                    id: mouse_area_button_load
                    z: 2
                    hoverEnabled: true
                    anchors.fill: parent
                    onEntered: {
                        parent.color = "#00b503"
                    }
                    onExited: {
                        parent.color = "#5b5b5b"
                    }
                }
            }

            Rectangle {
                id: button_save
                width: parent.height * 0.7
                height: 35
                anchors.right: parent.right
                anchors.rightMargin: parent.width * 0.05
                anchors.bottom: parent.bottom
                anchors.bottomMargin: parent.height * 0.05
                color: "#5b5b5b"
                border.color: "#353535"
                radius: 4
                Text {
                    id: text_button_save
                    text: qsTr("Save Image")
                    anchors.centerIn: parent
                    font.pixelSize: 9
                    color: '#ffffff'
                }
                MouseArea {
                    id: mouse_area_button_save
                    z: 2
                    hoverEnabled: true
                    anchors.fill: parent
                    onEntered: {
                        parent.color = "#00b503"
                    }
                    onExited: {
                        parent.color = "#5b5b5b"
                    }
                }
            }

        }

        Rectangle {
            id: rectangle_lower_section
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            width: parent.width
            height: Math.min(parent.height * 0.3, 200)
            color: "#424242"


            Rectangle {
                id: rectangle_buttons
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.top: parent.top
                anchors.topMargin: 0
                width: parent.width
                height: parent.height * 0.5
                color: "transparent"

                Rectangle {
                    id: button_histogram
                    anchors.left: parent.left
                    anchors.leftMargin: parent.width * 0.056
                    width: parent.width * 0.18
                    height: parent.height * 0.5
                    color: "#5b5b5b"
                    anchors.verticalCenter: parent.verticalCenter
                    border.color: "#353535"
                    radius: 4
                    Text {
                        id: text_button_histogram
                        text: qsTr("Histogram")
                        anchors.centerIn: parent
                        font.pixelSize: 9
                        color: '#ffffff'
                    }
                    MouseArea {
                        id: mouse_area_button_histogram
                        z: 2
                        hoverEnabled: true
                        anchors.fill: parent
                        onEntered: {
                            parent.color = "#00b503"
                        }
                        onExited: {
                            parent.color = "#5b5b5b"
                        }
                        onClicked: {
                            rectangle_selected_option.active = rectangle_option_gauss
                        }
                    }
                }

                Rectangle {
                    id: button_entropy
                    anchors.left: button_histogram.right
                    anchors.leftMargin: parent.width * 0.056
                    width: parent.width * 0.18
                    height: parent.height * 0.5
                    color: "#5b5b5b"
                    anchors.verticalCenter: parent.verticalCenter
                    border.color: "#353535"
                    radius: 4
                    Text {
                        id: text_button_entropy
                        text: qsTr("Entropy")
                        anchors.centerIn: parent
                        font.pixelSize: 9
                        color: '#ffffff'
                    }
                    MouseArea {
                        id: mouse_area_button_entropy
                        z: 2
                        hoverEnabled: true
                        anchors.fill: parent
                        onEntered: {
                            parent.color = "#00b503"
                        }
                        onExited: {
                            parent.color = "#5b5b5b"
                        }
                        onClicked: {
                            rectangle_selected_option.active = rectangle_option_entropy
                        }
                    }
                }

                Rectangle {
                    id: button_imopen
                    anchors.left: button_entropy.right
                    anchors.leftMargin: parent.width * 0.056
                    width: parent.width * 0.18
                    height: parent.height * 0.5
                    color: "#5b5b5b"
                    anchors.verticalCenter: parent.verticalCenter
                    border.color: "#353535"
                    radius: 4
                    Text {
                        id: text_button_imopen
                        text: qsTr("ImOpen")
                        anchors.centerIn: parent
                        font.pixelSize: 9
                        color: '#ffffff'
                    }
                    MouseArea {
                        id: mouse_area_button_imopen
                        z: 2
                        hoverEnabled: true
                        anchors.fill: parent
                        onEntered: {
                            parent.color = "#00b503"
                        }
                        onExited: {
                            parent.color = "#5b5b5b"
                        }
                        onClicked: {
                            rectangle_selected_option.active = rectangle_option_imopen
                        }
                    }
                }

                Rectangle {
                    id: button_convex
                    anchors.left: button_imopen.right
                    anchors.leftMargin: parent.width * 0.056
                    width: parent.width * 0.18
                    height: parent.height * 0.5
                    color: "#5b5b5b"
                    anchors.verticalCenter: parent.verticalCenter
                    border.color: "#353535"
                    radius: 4
                    Text {
                        id: text_button_convex
                        text: qsTr("Convex")
                        anchors.centerIn: parent
                        font.pixelSize: 9
                        color: '#ffffff'
                    }
                    MouseArea {
                        id: mouse_area_button_convex
                        z: 2
                        hoverEnabled: true
                        anchors.fill: parent
                        onEntered: {
                            parent.color = "#00b503"
                        }
                        onExited: {
                            parent.color = "#5b5b5b"
                        }
                        onClicked: {
                            rectangle_selected_option.active = rectangle_option_convex
                        }
                    }
                }
            }

            Rectangle {
                id: rectangle_selected_option
                height: parent.height * 0.5
                width: parent.width
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                color: "transparent"
                property var active: null

                Rectangle {
                    id: rectangle_option_gauss
                    color: "transparent"
                    visible: this === parent.active ? true : false
                    Label {
                        id: label_option_gauss_deviation
                        color: "#ffffff"
                        text: qsTr("Deviation")
                    }

                    TextInput {
                        id: input_gauss_deviation
                    }
                }

                Rectangle {
                    id: rectangle_option_entropy
                    color: "transparent"
                    visible: this === parent.active ? true : false
                }

                Rectangle {
                    id:rectangle_option_imopen
                    color: "transparent"
                    visible: this === parent.active ? true : false
                }

                Rectangle {
                    id:rectangle_option_convex
                    color: "transparent"
                    visible: this === parent.active ? true : false
                }
            }


            Rectangle {
                id: buttons_settings_border
                anchors.top: rectangle_buttons.bottom
                anchors.left: parent.left
                anchors.topMargin: -1
                width: parent.width
                height: 2
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

}
