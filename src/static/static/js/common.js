const LOCATION = {center: [27.567444, 53.893009], zoom: 10};


const POINTS = [
  {coordinates: [27.567444, 53.893009, ], size: '30px', title: 'Minsk, Belarus', onFastClick: () => alert('Coord: 27.567444, 53.893009')},
   
];

function diagram(props) {
  const div = document.createElement('div');

  const diagram = document.createElement('div');

  diagram.className = 'pie-marker';
  diagram.style.color = props.color;

  const gradient = [];
  let previous = 0;
  for (let i = 0; i < props.colors.length; i += 1) {
    const p = props.colors[i];
    const deg = (360 / 100) * p.percentage;
    gradient.push(`${p.color} ${previous}deg ${previous + deg}deg`);
    previous = previous + deg;
  }

  diagram.style.background = 'conic-gradient(' + gradient.join(', ') + ')';

  const title = document.createElement('div');
  title.innerHTML = props.title;
  title.className = 'pie-marker-title';

  div.appendChild(diagram);
  div.appendChild(title);

  return div;
}

function circle(props) {
  const circle = document.createElement('div');
  circle.classList.add('circle');
  circle.style.color = props.color;
  props.radius && circle.style.setProperty('--radius', props.radius);
  props.icon && circle.style.setProperty('--icon', props.icon);
  circle.title = props.title;
  return circle;
}

function icon(props) {
  const circle = document.createElement('div');
  circle.classList.add('icon');
  circle.style.color = props.color;
  circle.style.backgroundImage = `url(${props.icon})`;
  circle.style.setProperty('--size', props.size);

  if (props.title) {
    const title = document.createElement('div');
    title.innerHTML = props.title;
    title.className = 'icon-title';
    circle.appendChild(title);
  }

  return circle;
}