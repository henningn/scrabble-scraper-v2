import React from "react";

class Picture extends React.Component {

  render() {
    var img = 'web/image-' + this.props.move + '.jpg?' + this.props.time
    if (this.props.move == null) {
      return (
        <div className="card moves">
          <div className="card-body"></div>
        </div>
      );
    } else {
      return (
        <div className="card moves">
          <div className="card-body">
            <center><img src={img} width={'500px'} alt=" " /></center>
          </div>
        </div>
      );
    }
  }

}

export default Picture;
