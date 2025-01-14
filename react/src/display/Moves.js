import React from "react";

class Moves extends React.Component {

  render() {
    let items = []
    const align = {
      textAlign: 'right'
    }
    if (this.props.moves != null) {
      for (const [key, value] of Array.from(this.props.moves.entries())) {
        let name = value.slice(1, value.indexOf(':') + 1)
        let rest = value.slice(value.indexOf(':') + 1).trim()
        let sp = rest.split(' ')
        let img_link = "./web/image-" + (key + 1) + ".jpg"
        if (sp.length === 3) {
          items.push(<tr key={key + 1}>
            <td><a href={img_link} target="_scrabscrap_board">{key + 1}</a></td>
            <td>{name}</td>
            <td>{sp[0]}</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td style={align}>{sp[1]}</td>
            <td style={align}>{sp[2]}</td>
          </tr>)
        } else if (sp.length === 4) {
          items.push(<tr key={key + 1}>
            <td><a href={img_link} target="_scrabscrap_board">{key + 1}</a></td>
            <td>{name}</td>
            <td>{sp[0]}</td>
            <td>{sp[1]}</td>
            <td>&nbsp;</td>
            <td style={align}>{sp[2]}</td>
            <td style={align}>{sp[3]}</td>
          </tr>)
        } else {
          items.push(<tr key={key + 1}>
            <td><a href={img_link} target="_scrabscrap_board">{key + 1}</a></td>
            <td>{name}</td>
            <td>{sp[0]}</td>
            <td>{sp[1]}</td>
            <td>{sp[2]}</td>
            <td style={align}>{sp[3]}</td>
            <td style={align}>{sp[4]}</td>
          </tr>)
        }
        // items.push(<li key={key}>{value}</li>)
      }
    }
    return (
      <div className="card moves">
        <div className="card-body">
          <div className="tablemove">
            <table className="moves" >
              <tbody>
                {items}
              </tbody>
            </table>
          </div>
        </div>
      </div >
    );
  }

}

export default Moves;
