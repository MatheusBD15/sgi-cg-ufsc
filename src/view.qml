import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// gray1 = #eeeeee
// gray2 = #dddddd
// gray3 = #cccccc
// gray4 = #bbbbbb
// gray5 = #9a9a9a

// #eeeeee	(255,255,255)
// #bbbbbb
// #999999	(153,153,153)
// #666666	(102,102,102)


Rectangle {
    id: main
    width: 1920
    height: 1080
    visible: true
    color: "#eeeeee"

    Row {
        anchors.fill: parent

        Rectangle {
            id: menu
            color: "#bbbbbb"
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
                spacing: 30  // Space between items
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 20
                anchors.leftMargin: 20
                anchors.rightMargin: 20

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Objetos"
                    color: "black"
                }

                // ListView for scrolling items
                Rectangle {
                    id: listContainer
                    width: parent.width
                    height: 400  // Fixed height for ListView container
                    color: "#999999"
                    radius: 10
                    clip: true

                    ListView {
                        width: parent.width
                        height: parent.height
                        model: 1

                        delegate: Rectangle {
                            width: parent.width
                            height: 50
                            color: "#666666"
                            radius: 10
                            Text {
                                anchors.left: parent.left
                                anchors.top: parent.top
                                anchors.topMargin: 15
                                anchors.leftMargin: 10
                                text: "Item " + (index + 1)
                                color: "white"
                            }
                            Button {
                                id: deleteButton
                                height: 20
                                width: 20
                                anchors.right: parent.right
                                anchors.top: parent.top
                                anchors.topMargin: 15
                                anchors.rightMargin: 10
                                text: "X"
                            }
                            Button {
                                height: 20
                                width: 50
                                anchors.right: deleteButton.left
                                anchors.top: parent.top
                                anchors.topMargin: 15
                                anchors.rightMargin: 10
                                text: "Editar"
                            }

                        }

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AlwaysOn
                        }
                    }
                }

                Rectangle {
                    width: parent.width
                    height: 400  // Fixed height for ListView container
                    anchors.top: listContainer.bottom
                    anchors.topMargin: 10
                    color: "#999999"
                    radius: 10
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
