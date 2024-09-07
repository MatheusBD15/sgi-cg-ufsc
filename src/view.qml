import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: main
    width: 1920
    height: 1080
    visible: true
    color: "darkgrey"

    RowLayout {
        anchors.fill: parent

        Rectangle {
            id: menu
            color: "gray"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 20
            radius: 10
        }

        Rectangle {
            id: canvas
            color: 'black'
            Layout.preferredWidth: 1280
            Layout.preferredHeight: 720
            Layout.rightMargin: 20

        }
    }
}