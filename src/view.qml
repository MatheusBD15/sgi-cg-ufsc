import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: main
    width: 1920
    height: 1080
    visible: true
    color: "darkgrey"

    Row {
        anchors.fill: parent

        Rectangle {
            id: menu
            color: "gray"
            width: 400  // Fixed width for menu
            height: parent.height
            radius: 10
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            anchors.topMargin: 20
            anchors.leftMargin: 20

            Column {
                width: parent.width
                spacing: 10  // Space between items
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 20
                anchors.leftMargin: 20
                anchors.rightMargin: 20



                // Static header
                Rectangle {
                    width: parent.width
                    height: 100
                    color: "red"
                    Text {
                        anchors.centerIn: parent
                        text: "Header"
                        color: "white"
                    }
                }

                // ListView for scrolling items
                Rectangle {
                    width: parent.width
                    height: 400  // Fixed height for ListView container
                    color: "gray"
                    border.color: "black"
                    border.width: 1

                    ListView {
                        width: parent.width
                        height: parent.height
                        model: 20

                        delegate: Rectangle {
                            width: parent.width
                            height: 50
                            color: "lightgray"
                            border.color: "black"
                            border.width: 1
                            Text {
                                anchors.centerIn: parent
                                text: "Item " + (index + 1)
                                color: "black"
                            }
                        }

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AlwaysOn
                        }
                    }
                }

                // Static footer
                Rectangle {
                    width: parent.width
                    height: 50
                    color: "blue"
                    Text {
                        anchors.centerIn: parent
                        text: "Footer"
                        color: "white"
                    }
                }
            }
        }

        Rectangle {
            id: canvas
            color: 'black'
            width: 1280
            height: 720
            border.color: "white"
            border.width: 2
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: 100
            radius: 10
        }
    }
}
